<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Existing API and behavior baseline

This combines the original static inventory with M1's executable baseline. The
Windows x64 core checks, both Minecraft 26.3 loader builds, and required GameTests
pass. Optional GameTest failures remain, so M1 and broader parity are PARTIAL;
see Qualification.md for scope and evidence.

## Surface layers

| Surface | Existing functionality | Source and qualification starting point |
| --- | --- | --- |
| Language/globals | Cobalt standard libraries, bit32, error-info extensions, _HOST, BIOS globals | core/lua/CobaltLuaMachine.java; bios.lua; preserve actual Lua behavior |
| os | Computer ID/label, time/epoch/date, timers/alarms, queued events, reboot/shutdown; BIOS adds event pulls/run/loadAPI | core/apis/OSAPI.java and bios.lua; terminate bypasses event filter |
| fs + io + handles | Virtual mounts, path traversal, read/write/text/binary handles, listing/copy/delete, capacity and read-only checks | core/apis/FSAPI.java, apis/handles/, core/filesystem/, ROM fs.lua/io.lua |
| term + window | Cursor/colors/palette, text/blit, scrolling, terminal redirection and windows | core/apis/TermAPI.java, TermMethods.java, core/terminal/, ROM term.lua/window.lua |
| redstone / rs | Digital, analog/analogue and bundled input/output | core/apis/RedstoneAPI.java and RedstoneMethods.java; retain spelling aliases |
| peripheral | Discovery/types/methods, calls/wrapping, attach/detach and generic capabilities | core/apis/PeripheralAPI.java, ROM peripheral.lua, shared/peripheral/ |
| http | Policy-controlled requests, URL checking and websocket operations, events/handles; configurable availability | core/apis/HTTPAPI.java, apis/http/, ROM http/http.lua |
| turtle | Movement/turning; dig/place/attack; detect/inspect/compare; slots/item detail; suck/drop/transfer; fuel/refuel; equip/craft | shared/turtle/apis/TurtleAPI.java, ROM apis/turtle/turtle.lua, command classes and upgrades |
| pocket | Pocket upgrade equip/unequip on supported devices | shared/pocket/apis/PocketAPI.java and pocket host classes |
| commands | Command-computer execution and world/block query helpers, permission-sensitive | shared/computer/apis/CommandAPI.java and ROM apis/command/commands.lua; not ordinary computer authority |
| disk | Disk presence/mount/audio/labels/computer ID wrappers | ROM disk.lua; shared/peripheral/diskdrive/ |
| rednet + gps | Modem-backed messaging/hosting/lookup and positioning protocol | ROM rednet.lua/gps.lua, modem peripherals; not built-in absolute robot position |
| speaker / printer / monitor | Audio queues, page output, remote terminal methods and monitor events | shared/peripheral/speaker/, printer/, monitor/ |
| inventory / fluid / energy | Generic peripheral query/transfer adapters where supported by loader | shared/peripheral/generic/methods/, loader implementations; inventory is not villager offers |
| colors/colours + keys | Constants and color helpers, keyboard key mappings | ROM colors.lua/colours.lua/keys.lua; constants/aliases need runtime enumeration |
| settings + help | Persistent settings/definitions and help paths/topics | ROM settings.lua/help.lua |
| textutils + paintutils + vector | Serialization/JSON/formatting, image drawing, vectors | ROM textutils.lua/paintutils.lua/vector.lua |
| parallel | Cooperative Lua coroutine event fan-out | ROM parallel.lua; not separate OS threads or a second VM |
| shell + multishell | Program lookup, arguments, environment, completion, tabs/windows | ROM programs/shell.lua, programs/advanced/multishell.lua; injected environment APIs |
| cc.* modules | expect, completion/shell.completion, pretty, strings, audio.dfpwm, image.nft, require, base64 | ROM modules/main/cc/; cc.internal.* is implementation detail |
| ROM utilities | Startup/autorun, editor, file tools, turtle utilities, HTTP runners, rednet apps and games | ROM programs/ and rom/startup.lua; preserve stock files |
| Addon Java contracts | LuaFunction, ILuaAPI/APIFactory, IComputerSystem, MethodResult, IPeripheral, generic APIs, turtle/pocket upgrades | core-api and common-api; preserve interfaces and receiver/result semantics |

Paths abbreviated above are under projects/core/src/main/java/dan200/computercraft/
or projects/common/src/main/java/dan200/computercraft/ as appropriate. ROM is under
projects/core/src/main/resources/data/computercraft/lua/rom/.

## Reproducible native method census

[NativeApiInventory.csv](NativeApiInventory.csv) enumerates production Java
`@LuaFunction` declarations and named aliases with source license/line, signature, declared
module hint and main-thread/unsafe flags. Regenerate with:

```powershell
python tools/InventoryApis.py
python tools/InventoryApis.py --check
```

This is a declaration census, not a runtime-export census: inherited methods,
API getNames(), ROM wrappers, dynamically generated command methods, constants,
returned objects and addon registration affect the final surface. The next gate
must capture those from a booted stock host and link each contract to behavior
tests. Do not present CSV rows as globally callable functions.

## Behavior to preserve and measure first

1. Boot ordinary/advanced/pocket/turtle/command computers on both loaders; record
   globals, API tables, aliases, peripheral method exports and availability policy.
2. Capture signatures, result arity/types, nil/empty behavior, failure messages,
   yielding behavior and emitted events. MethodResult callbacks and task_complete
   are part of the API, not just Java implementation details.
3. Run existing ROM and Java suites, then headless GameTests. Include file mounts,
   read-only errors, terminal redirects, peripheral detach during calls, disabled
   HTTP, redstone, timers/terminate, fuel exhaustion and obstructed movement.
4. Save/reload a baseline world; verify computer IDs, disks, turtle state and stored
   startup files. Record fixture/config/loader/artifact hashes with evidence.
5. Give every capability a future Luau status: preserve on Lua, adapt for Luau,
   explicitly unsupported, or deferred. No wholesale parity claim until measured.

No existing self/Enum/service facade or villager offer query was found in the
reviewed baseline. These remain additive future features, not renamed stock APIs.

## M1 executable capture (2026-10-15)

The new core `BaselineTest.RuntimeInventoryAndEntrypoints` boots the real BIOS and
captures exported methods from the resulting Lua environment into
`projects/core/build/tmp/testFiles/baseline/CoreRuntimeInventory.json`. It also
checks shell argument boundaries and success/error behavior separately from
os.run. The probe passes and its [core capture](evidence/M1-20261015/CoreRuntimeInventory.json)
matches all 82 expected native core names. The two loader GameTest servers also
capture actual normal/advanced computer and normal-turtle exports.

After running the test, compare the observed exports against the existing census:

```text
python tools/ValidateRuntimeInventory.py projects/core/build/tmp/testFiles/baseline/CoreRuntimeInventory.json
```

The comparator checks native core API method names, including declared spelling
aliases and inherited TermMethods/RedstoneMethods. It treats missing APIs/methods
as incomplete coverage. It does not qualify signatures, device/peripheral methods,
loader registration, or behavior. Those remain separate tests and evidence gates.
Its negative-path unit check uses synthetic data and is tooling evidence only.

| Host profile | Fabric 26.3 | NeoForge 26.3 | Native names matched |
| --- | --- | --- | --- |
| Normal computer | PASS | PASS | 82 core |
| Advanced computer | PASS | PASS | 82 core |
| Normal turtle | PASS | PASS | 82 core + 44 turtle |

Raw captures and machine-readable comparisons are under
[Fabric evidence](evidence/M1-20261015/Fabric/) and
[NeoForge evidence](evidence/M1-20261015/NeoForge/). Device capability and terminal
color observations match the fixture hardware. ROM wrappers add methods beyond
the native census; the comparison requires every selected native name to exist,
not equality between Java declarations and the whole ROM surface.

Execution probes establish: shell.execute/os.run return execution success even
when a chunk returns false; os.run writes into its supplied environment; shell.run
tokenises arguments while shell.execute preserves boundaries; filtered events
retain trailing arguments/nil arity; terminate bypasses filters and pullEventRaw
receives it; main-thread tasks run on the designated host thread; reboot/unload
invoke lifecycle cleanup; shutdown closes deliberately unclosed mounted channels.

The actual async event is **task_complete**, despite inherited ILuaContext/LuaTask
Javadoc spelling it task_completed. The initial new probe exposed that mismatch;
only the probe and fork documentation were corrected. Existing runtime code and
the CCPL API files were left unchanged.
