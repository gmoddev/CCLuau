// SPDX-FileCopyrightText: 2026 gmoddev
//
// SPDX-License-Identifier: MPL-2.0

package dan200.computercraft.core.computer;

import dan200.computercraft.api.lua.ILuaAPI;
import dan200.computercraft.api.lua.ILuaContext;
import dan200.computercraft.api.lua.LuaException;
import dan200.computercraft.api.lua.LuaFunction;
import dan200.computercraft.api.lua.MethodResult;
import dan200.computercraft.core.ComputerContext;
import dan200.computercraft.core.TestFiles;
import dan200.computercraft.core.computer.mainthread.MainThread;
import dan200.computercraft.core.computer.mainthread.MainThreadConfig;
import dan200.computercraft.core.filesystem.MemoryMount;
import dan200.computercraft.core.filesystem.WritableFileMount;
import dan200.computercraft.core.terminal.Terminal;
import dan200.computercraft.test.core.computer.BasicEnvironment;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;

/** Execution-critical baseline probes running the real Cobalt BIOS and shell. */
@Timeout(30)
public class BaselineTest {
    @Test
    public void RuntimeInventoryAndEntrypoints() throws IOException {
        var Probe = new BaselineProbe();
        ComputerBootstrap.run("""
            assert(type(shell.execute) == 'function' and type(os.run) == 'function')
            assert(type(require('cc.require').make) == 'function')
            assert(rs == redstone and colors.red == colours.red and colors.gray == colours.grey)
            assert(self == nil and Enum == nil and computer == nil)
            local function GetNames(Value)
                local Names = {}
                for Name, Entry in pairs(Value) do
                    if type(Entry) == 'function' then Names[#Names + 1] = Name end
                end
                table.sort(Names)
                return Names
            end
            local Inventory = { GlobalFunctions = GetNames(_G), Apis = {} }
            for _, Name in ipairs({ 'os', 'fs', 'term', 'redstone', 'peripheral', 'http',
                'shell', 'parallel', 'textutils', 'settings' }) do
                if type(_ENV[Name]) == 'table' then Inventory.Apis[Name] = GetNames(_ENV[Name]) end
            end
            baseline.Capture(textutils.serializeJSON(Inventory))
            local File = assert(fs.open('Child.lua', 'w'))
            File.write('local A, B = ...; assert(A == "arg 1" and B == "arg2"); '
                .. 'assert(arg[0] == "Child.lua"); return false')
            File.close()
            -- Shell returns execution success, not the chunk's return value.
            assert(shell.execute('Child.lua', 'arg 1', 'arg2') == true)
            local Environment = { Marker = 73 }
            File = assert(fs.open('Run.lua', 'w'))
            File.write('local A = ...; assert(Marker == 73 and A == "packed arg"); Seen = true; return false')
            File.close()
            assert(os.run(Environment, 'Run.lua', 'packed arg') == true and Environment.Seen)
            File = assert(fs.open('Failure.lua', 'w'))
            File.write('error("expected baseline failure", 0)')
            File.close()
            assert(os.run({}, 'Failure.lua') == false)
            assert(shell.execute('Failure.lua') == false)
            assert(shell.run('Child.lua "arg 1" arg2') == true)
            """, Computer -> Computer.addApi(Probe), 10);
        assertEquals(1, Probe.Snapshots.size());
        var Output = TestFiles.get("baseline/CoreRuntimeInventory.json");
        Files.createDirectories(Output.getParent());
        Files.writeString(Output, Probe.Snapshots.getFirst() + "\n", StandardCharsets.UTF_8);
        assertEquals(1, Probe.Starts.get());
        assertEquals(1, Probe.Stops.get());
    }

    @Test
    public void EventFilteringTerminationAndMainThreadCalls() {
        var Probe = new BaselineProbe();
        ComputerBootstrap.run("""
            os.queueEvent('BaselineIgnored', 'discarded')
            os.queueEvent('BaselineWanted', 42, nil, 'tail')
            local Event = table.pack(os.pullEvent('BaselineWanted'))
            assert(Event.n == 4 and Event[1] == 'BaselineWanted' and Event[2] == 42)
            assert(Event[3] == nil and Event[4] == 'tail')
            os.queueEvent('terminate')
            local Ok, Reason = pcall(os.pullEvent, 'BaselineNever')
            assert(not Ok and Reason == 'Terminated')
            os.queueEvent('terminate')
            assert(os.pullEventRaw('BaselineNever') == 'terminate')
            assert(baseline.OnMainThread() == 'MainThread')
            local TaskId = baseline.QueueMainThread()
            local Name, Id, Success, Result = os.pullEvent('task_completed')
            assert(Name == 'task_completed' and Id == TaskId and Success and Result == 'Queued')
            """, Computer -> Computer.addApi(Probe), 10);
        assertEquals(2, Probe.MainThreadCalls.get());
        assertEquals(1, Probe.Stops.get());
    }

    @Test
    public void FilesystemAndStartupSurviveFreshHost(@TempDir Path Root) throws IOException {
        // This is an isolated core filesystem fixture, not Minecraft block/NBT persistence.
        Files.writeString(Root.resolve("startup.lua"), """
            local Ok, Reason = pcall(function()
                local Previous = 0
                if fs.exists('Boots.txt') then
                    local File = assert(fs.open('Boots.txt', 'r'))
                    Previous = assert(tonumber(File.readAll()))
                    File.close()
                end
                local File = assert(fs.open('Boots.txt', 'w'))
                File.write(tostring(Previous + 1))
                File.close()
                assert(os.getComputerID() == 0)
                assert(fs.getDrive('startup.lua') == 'hdd')
            end)
            assertion.assert(Ok, Reason)
            os.shutdown()
            """, StandardCharsets.UTF_8);
        for (var Boot = 1; Boot <= 2; Boot++) {
            var Probe = new BaselineProbe();
            ComputerBootstrap.run(new WritableFileMount(Root.toFile(), 100000), Computer -> Computer.addApi(Probe), 10);
            assertEquals(Integer.toString(Boot), Files.readString(Root.resolve("Boots.txt")));
            assertEquals(1, Probe.Starts.get());
            assertEquals(1, Probe.Stops.get());
        }
    }

    @Test
    public void RebootAndUnloadReleaseResources() throws Exception {
        var Mount = new MemoryMount().addFile("startup.lua", """
            if fs.exists('Rebooted') then
                baseline.Capture('SecondBoot')
                os.pullEvent('BaselineHold')
            else
                local File = assert(fs.open('Rebooted', 'w'))
                File.write('yes')
                File.close()
                os.reboot()
            end
            """);
        var Environment = new BasicEnvironment(Mount);
        var Scheduler = new MainThread(new MainThreadConfig.Basic(Integer.MAX_VALUE, Integer.MAX_VALUE));
        var Context = ComputerContext.builder(Environment).mainThreadScheduler(Scheduler).build();
        var Device = new Computer(Context, Environment, new Terminal(51, 19, true), 91);
        var Probe = new BaselineProbe();
        Device.addApi(Probe);
        try {
            Device.turnOn();
            var Deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(15);
            while (Probe.Snapshots.isEmpty() && System.nanoTime() < Deadline) {
                Device.tick();
                Scheduler.tick();
                Thread.sleep(10);
            }
            assertEquals(List.of("SecondBoot"), Probe.Snapshots);
            assertEquals(2, Probe.Starts.get());
            assertEquals(1, Probe.Stops.get());
            assertEquals(91, Device.getID());
            Device.unload();
            Deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(5);
            while ((Device.isOn() || Probe.Stops.get() < 2) && System.nanoTime() < Deadline) {
                Device.tick();
                Scheduler.tick();
                Thread.sleep(10);
            }
            assertFalse(Device.isOn());
            assertEquals(2, Probe.Stops.get());
        } finally {
            Device.unload();
            assertTrue(Context.close(5, TimeUnit.SECONDS), "Computer workers must terminate");
        }
    }

    public static class BaselineProbe implements ILuaAPI {
        final AtomicInteger Starts = new AtomicInteger();
        final AtomicInteger Stops = new AtomicInteger();
        final AtomicInteger MainThreadCalls = new AtomicInteger();
        final List<String> Snapshots = new CopyOnWriteArrayList<>();
        final Thread Owner = Thread.currentThread();

        @Override
        public String[] getNames() {
            return new String[]{ "baseline" };
        }

        @Override
        public void startup() {
            Starts.incrementAndGet();
        }

        @Override
        public void shutdown() {
            Stops.incrementAndGet();
        }

        @LuaFunction
        public final void Capture(String Payload) {
            Snapshots.add(Payload);
        }

        @LuaFunction
        public final MethodResult OnMainThread(ILuaContext Context) throws LuaException {
            return Context.executeMainThreadTask(() -> {
                if (Thread.currentThread() != Owner) throw new LuaException("[Baseline:Thread] Wrong thread");
                MainThreadCalls.incrementAndGet();
                return new Object[]{ "MainThread" };
            });
        }

        @LuaFunction
        public final long QueueMainThread(ILuaContext Context) throws LuaException {
            return Context.issueMainThreadTask(() -> {
                if (Thread.currentThread() != Owner) throw new LuaException("[Baseline:Thread] Wrong thread");
                MainThreadCalls.incrementAndGet();
                return new Object[]{ "Queued" };
            });
        }
    }
}
