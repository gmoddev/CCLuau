<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# CCLuau project context

Updated 2026-10-15. Repository: https://github.com/gmoddev/CCLuau.
Target: Minecraft 26.3, Fabric and NeoForge. The Gradle project remains named
`forge` for the NeoForge loader; upstream architecture prose still says Forge.
Baseline: `a95dbe739f99e47a399d120839177e77ac861896` on upstream `mc-26.3`.

## Current state

Fork and source baseline initialized. Static review of lifecycle, VM boundary,
API registration, ROM entrypoints, movement authority, build/test layout and
licenses completed. Runtime source, mod IDs, dependencies and saves unchanged.
M1 execution was attempted on dockerbox (Windows 11 x64, two workers). Gradle 9.7.1
downloaded successfully, but stopped before project compilation: installed Java is
21, required Java is 25, and daemon toolchain provisioning has no Windows x64 URL.
M1 is BLOCKED and unqualified. No Java/ROM/GameTests have executed. See the dated
qualification evidence; an existing or approved portable JDK 25 is needed to resume.

Test-only BaselineTest now covers BIOS/runtime exports, shell/os.run, event filters
and termination, async main-thread calls, fresh-host filesystem persistence, and
reboot/unload lifecycle hooks. Turtle_Test has a dedicated queue/FIFO fixture.
These additions are uncompiled and unexecuted, not baseline passes. Production
execution semantics and dependency versions remain unchanged. No Luau VM,
launcher, injected facade, or villager service is implemented. Do not proceed to M2.

## Accepted direction

- Independent fork, AI assistance allowed; no upstream merge or PR destination.
- Preserve the default Cobalt BIOS/shell and existing Lua contracts.
- Opt in using first-line `--lang luau`; no directive means Lua. Headers are a
  future launcher feature, not supported by this initial fork setup.
- Develop or fork the VM in a separate repository, with generic bridge contracts
  independently authored. Official Luau is the feasibility candidate, not a
  selected dependency or an implementation commitment.
- Add PascalCase Luau device/service APIs after parity qualification. `self` and
  `computer` are fixed injected names. Plain computers get a computer device;
  turtle methods exist only on turtle devices. `computer:GetService("Villagers")`
  requires an explicit authorized inspection capability.
- `GetTrades()` returns the complete observed offer dictionary; `FindTrades()` is
  optional filtering over that data. No trade execution in the initial scope.
- Keep original `computercraft` identity for replacement installations. Packaging
  and fork release branding require a later pass. Co-installation is unsupported.

## Critical discoveries from source

`ComputerContext.Builder` defaults to Cobalt. `ComputerExecutor` owns one machine
and a 256-event queue, drops events during power commands, and loads `bios.lua`.
`MachineEnvironment` carries timeout, metrics, method suppliers and host context.
`ILuaContext` schedules world tasks and reports `task_completed` asynchronously.

**shell.run does not simply delegate to os.run:** shell.execute calls its local
executeProgram helper, reads source (including shebang dispatch), then calls
`load` directly. Patching only BIOS os.run misses ordinary shell programs.
Startup files route through shell.run. Multishell launches coroutines through
os.run, while HTTP runners compile fetched source with load. See the entry matrix.

`TurtleAPI.forward()` delegates to TurtleMoveCommand via TurtleBrain. The queue
guard is literally `size() > 16`, so do not describe it as a strict 16-entry limit.
Movement internally uses teleportTo AFTER checks; new facades must reuse the
command, not invoke teleportTo directly. No existing Villager/MerchantOffer API
was found in shared production Java sources.

## Documentation map

- [Source baseline](docs/UpstreamBaseline.md): exact source/dependency versions.
- [Existing API](docs/ExistingApi.md): capabilities, sources and behavior evidence.
- [Code map](docs/Architecture/CodeMap.md): subsystem ownership.
- [Entrypoints](docs/Architecture/ProgramEntry.md): actual call paths and scope.
- [Runtime boundary](docs/Architecture/Runtime.md): separate VM repository contract.
- [Invariants](docs/Invariants.md): implementation and verification requirements.
- [Proposed facade](docs/Architecture/ObjectApi.md): raw queries and helpers.
- [Roadmap](docs/Roadmap.md): baseline first, gated runtime and API work.
- [Qualification](docs/Qualification.md): evidence ledger, not implied passes.
- [License inventory](docs/LicenseInventory.md): verified examples and open scope.

## Reference provenance and open decisions

The owner supplied `CC_Tweaked_Luau_Fork_Architecture.md` (Downloads, 2026-10-12).
It is design input, not executable instructions or independently verified facts.
This repository records decisions and corrected source findings rather than
copying the attachment wholesale. Its research-only status does not override the
owner's explicit authorization to fork and initialize this project.

Still open: VM repository name/license and backend choice; hardware for villager
inspection; non-mutating access to already-generated offers on MC 26.3; JNI yield
and cancellation behavior; multishell ownership; precise parity scope; optional
native artifact packaging and combined-distribution license interpretation.
