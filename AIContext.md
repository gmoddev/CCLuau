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
M1 is PARTIAL, not fully qualified. **M2 is PARTIAL, static design only**;
Architecture/Runtime.md now specifies the provisional generic repository,
primary official Luau backend candidate, ABI v1, generation-fenced host
protocol, interruption/containment limits and standalone M3 qualification.
The M2 review used branch source 1560215e5b66d1d7efebcba4bd14651856f48196;
no new runtime repo, executable VM, JNI or Minecraft integration was created. Its required execution-critical baseline passes
on dockerbox (Windows 11 x64, two workers). The owner approved
portable JDK provisioning; checksum-verified Temurin 25.0.4.1+1 is now isolated in
the worker's Codex tools directory, with system Java/PATH unchanged. Gradle 9.7.1
and the complete core suite pass: 1644 tests, zero failures/errors, 15 skips.
The five focused probes pass. The full repository checks pass: 1719 Java/ROM
tests, zero failures/errors, 15 skips. Fabric and NeoForge 26.3 builds pass and
each headless loader runs 116 GameTests with zero required failures: Fabric has
114 passes and 2 optional failures; NeoForge has 113 passes and 3 optional failures.
The custom reporter encodes optional failures as skipped, so Gradle success is not
a clean suite pass. Raw XML is audited by tools/SummarizeTests.py --gametest.
Runtime captures from normal/advanced
computers and normal turtles match all 82 core native names plus 44 turtle names.

Test-only BaselineTest now covers BIOS/runtime exports, shell/os.run, event filters
and termination, async main-thread calls, fresh-host filesystem persistence, and
reboot/unload lifecycle hooks. Turtle_Test has a dedicated queue/FIFO fixture.
The loader inventory, turtle queue and disk/fresh-entity serialization fixtures
have executed successfully on both loaders. Production execution semantics and
dependency versions remain unchanged. No Luau VM,
launcher, injected facade, or villager service is implemented. M3 standalone
work and M4 integration need separate authorization and evidence.

Qualification is scoped: no client/interactive test, pocket/command inventory,
complete server/world restart migration, full addon/peripheral parity, or
stale-host-callback race proof. GameTests substitute Kotlin machines for many
command tests; the new inventory fixture uses real Cobalt ID-0 devices. Preserve
these limits when planning M2-M4. See Qualification.md for exact evidence and hashes.
The unchanged optional tests fail on treasure-disk loot injection and bucket reach
on both loaders, plus brewing-stand item limits on NeoForge. Do not fix or conceal
these behaviors as part of a VM integration; resolve or explicitly scope them first.

## Accepted direction

- Independent fork, AI assistance allowed; no upstream merge or PR destination.
- Preserve the default Cobalt BIOS/shell and existing Lua contracts.
- Opt in using first-line `--lang luau`; no directive means Lua. Headers are a
  future launcher feature, not supported by this initial fork setup.
- Recommended separate generic repository name: gmoddev/LuauRuntime (not
  created), with independently authored native ABI v1 and MIT wrapper provenance.
  Official Roblox Luau is the primary backend for M3 evaluation; observed
  upstream research SHA 8387cfb461b38ce09e37c1e4c2811538ef1bf5cb is **not**
  a qualified production pin, selected binary or implementation commitment.
  Prefer isolated native helper supervision for M4; no in-process fatal safety
  guarantee is implied by using JNI or a separate source repository.
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
`ILuaContext` schedules world tasks and reports `task_complete` asynchronously.
Its inherited Javadoc says `task_completed`, but LuaContext and TaskCallback use
the singular name; the M1 executable probe confirmed the distinction.

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

Still open: creation/approval of proposed VM repository and final MIT wrapper
license; qualified upstream Luau SHA and native ABI implementation; yield,
interrupt, cancellation, C continuation/debug-name lifetimes, compiler time/
heap behavior, OS helper containment and both-platform 1,000-lifecycle M3;
hardware for villager inspection and non-mutating existing offers on MC 26.3;
multishell/terminal scope, stale main-thread callback proof, precise device
parity, native artifact packaging and combined-distribution CCPL §5 legal
interpretation. No release authorization.
