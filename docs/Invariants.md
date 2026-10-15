<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Implementation invariants

Baseline constraints and future acceptance requirements. Future requirements are
not claims about protections already implemented by upstream.

| ID | Rule | Evidence / verification obligation |
| --- | --- | --- |
| I01 | Minecraft remains 26.3; preserve mod ID, registry IDs, saved computer data and existing Lua method names | Pinned catalog; compare old world/ROM behavior on both loaders |
| I02 | No directive means Cobalt. Cobalt owns BIOS/shell. Luau failure never silently runs source as Lua | ComputerContext default and ComputerExecutor boot; future dispatch tests |
| I03 | Preserve event filters, terminate, timers, asynchronous host calls, shell arguments/results and redirection | CobaltLuaMachine, BIOS, MethodResult and actual shell load path; behavior tests |
| I04 | World access/mutation runs through authorized server-thread host calls, not VM/JNI worker callbacks | ILuaContext; core has no Minecraft dependency |
| I05 | Move/turn facades use existing turtle commands and queue; preserve fuel, obstruction, loaded-world and protection checks | TurtleAPI -> TurtleBrain -> TurtleMoveCommand; partial move tests |
| I06 | A multi-step move stops at first failure with explicit completed count; no hidden dig, refuel, retry or rollback | Proposed count 1..64, serialize stepwise, cancel between steps |
| I07 | Each future CCLuau session carries ComputerId, BootGeneration and SessionId; revoke before close, fence at host-task admission, immediately before world side effects and again on completion; discard stale replies | M1 does not prove callback races; M4 reboot/unload/cancel and already-entered-task tests. Generic ABI uses opaque handles without Minecraft types |
| I08 | Lua and Luau heaps, module caches, closures and coroutines remain separate | Bounded primitive/table copies and opaque capabilities only |
| I09 | CPU, heap, compiler input, events, callbacks, result depth/size and host requests are bounded by explicitly qualified mechanisms; do not promise exact instructions/slice yield from safepoint interrupts | Existing queue 256/turtle guard size > 16; M3 compiler, allocator, watchdog, serialization and helper-process exhaustion tests |
| I10 | Native sessions close once without freeing executing callbacks; cancellation revokes authority before cleanup, and fatal native hangs/crashes must be contained outside the Minecraft process before integration | M3 1,000 lifecycles per x64 OS, concurrent cancel/close, OOM, crash/hang helper survival; M4 unload/reboot race proof |
| I11 | Scripts receive no Java reflection, process/native loading, host filesystem or untrusted bytecode loading | Separate VM sandbox qualification; compile trusted source with pinned compiler |
| I12 | Exactly one initial Luau foreground child owns a generation-fenced computer terminal lease; the Cobalt launcher yields while it runs and always regains control on completion/failure/terminate | M4 foreground lease/revocation, completion-ticket integrity and no multishell/parallel compatibility promise before qualification |
| I13 | Villager reads expose already-generated reachable offers without generating offers or mutating merchant state | Main-thread snapshots; qualify MC 26.3 lazy-generation access before code ships |
| I14 | GetTrades is the raw complete observed offer dictionary; FindTrades cannot reveal extra data or mutate it | Same snapshot/version, component IDs/levels, no display-name matching |
| I15 | Availability and prices are observations, not reservations or promises of player-specific discounts | Include tick/version and price context; no ExecuteTrade in initial scope |
| I16 | Naming is PascalCase for new owned identifiers; legacy contracts and fixed globals stay intact | AGENTS.md; no mass cosmetic refactors |
| I17 | Failures stay in computer terminal/server/tool logs; no modal dialogs, focus changes or game overlays | Captured/headless commands and bounded diagnostics with [System:SubSystem] |
| I18 | Preserve licenses/attribution; independently authored generic VM remains outside the CCPL fork with no copied CC implementation; separation never asserts combined-distribution license clearance | Per-file SPDX/REUSE, Luau MIT notices and CCPL §5 dependency/packaging legal review before release |
| I19 | Fork work never targets upstream merge/review/push | origin/main; upstream push disabled; fork contribution links |
| I20 | Report static, unit, integration, live and release evidence separately | docs/Qualification.md; no claim of builds from source inspection |

Changing an invariant requires a recorded decision, compatibility impact, and
updated verification plan. Avoid weakening a rule to make an unqualified prototype
look complete.
