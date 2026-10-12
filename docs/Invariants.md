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
| I07 | Each future session/handle carries computer ID, boot generation and session identity; revoke and discard stale completions | Reboot/unload/cancel tests; do not pass raw native pointers to scripts |
| I08 | Lua and Luau heaps, module caches, closures and coroutines remain separate | Bounded primitive/table copies and opaque capabilities only |
| I09 | CPU, heap, compiler input, events, callbacks, result depth/size and host requests are bounded | Existing event queue is 256; turtle guard size > 16; prove new quotas and pathological loops |
| I10 | Native sessions close once; worker cancellation and allocation ownership remain safe on all exits | Repeated create/close, callback interruption, allocation failure and unload evidence |
| I11 | Scripts receive no Java reflection, process/native loading, host filesystem or untrusted bytecode loading | Separate VM sandbox qualification; compile trusted source with pinned compiler |
| I12 | Exactly one initial Luau foreground session owns a computer terminal; Lua launcher yields while it runs | No multishell/parallel compatibility promise before qualification |
| I13 | Villager reads expose already-generated reachable offers without generating offers or mutating merchant state | Main-thread snapshots; qualify MC 26.3 lazy-generation access before code ships |
| I14 | GetTrades is the raw complete observed offer dictionary; FindTrades cannot reveal extra data or mutate it | Same snapshot/version, component IDs/levels, no display-name matching |
| I15 | Availability and prices are observations, not reservations or promises of player-specific discounts | Include tick/version and price context; no ExecuteTrade in initial scope |
| I16 | Naming is PascalCase for new owned identifiers; legacy contracts and fixed globals stay intact | AGENTS.md; no mass cosmetic refactors |
| I17 | Failures stay in computer terminal/server/tool logs; no modal dialogs, focus changes or game overlays | Captured/headless commands and bounded diagnostics with [System:SubSystem] |
| I18 | Preserve licenses and attribution; VM code is independently maintained outside the fork | Per-file SPDX/REUSE review; separation does not waive combined dependency obligations |
| I19 | Fork work never targets upstream merge/review/push | origin/main; upstream push disabled; fork contribution links |
| I20 | Report static, unit, integration, live and release evidence separately | docs/Qualification.md; no claim of builds from source inspection |

Changing an invariant requires a recorded decision, compatibility impact, and
updated verification plan. Avoid weakening a rule to make an unqualified prototype
look complete.
