<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# CCLuau roadmap

Target Minecraft 26.3, Fabric and NeoForge. Deliver baseline understanding and
functionality first. The architecture attachment is an RFC; this roadmap records
the owner's selected direction and source corrections. Each gate needs recorded
evidence in Qualification.md before dependent integration work is declared done.

| Milestone | Deliverables | Exit criteria / current state |
| --- | --- | --- |
| M0 Fork foundation | mc-26.3 history/baseline, main, agent policy, context, source map, invariants, initial API/entry census | Repository/docs initialized; static checks only; no runtime change |
| M1 Existing API and functionality | Build stock baseline; execute Java/ROM suites; runtime export/alias/constants census; per-API contracts/results/events; headless loader tests; save/load fixtures | PARTIAL on 2026-10-15: builds and 1719 Java/ROM checks pass (15 skipped); all required GameTests and new probes pass. Fabric has 114 passes/2 optional failures, NeoForge 113/3. Runtime inventories and isolated persistence verified; optional behaviors, broader parity and full world restart remain unqualified. See Qualification.md |
| M2 Runtime design and repository boundary | Select/name separate VM repo, provenance/license, generic ABI, source/compiler pin, session state machine, budgets and cancellation design; host adapter ownership | Written contracts and backend feasibility decision; no CCPL code copied outside fork; PLANNED |
| M3 Standalone VM proof | Official Luau or justified alternative, sandbox, compile/resume/yield, host requests, interruptions, memory accounting, copied values, native artifact manifest | Windows/Linux x64 evidence; tight loops, callback cancellation, OOM, malformed/cyclic values and 1000 lifecycles pass; PLANNED |
| M4 Opt-in developer runner | Managed child session, explicit luau command, yielded Cobalt caller, terminal ownership, event/host bridge, generation fencing | Returns/errors/terminate/reboot/unload work without BIOS corruption; Lua baseline green; both loaders qualified; PLANNED |
| M5 Program directives | First-line classification, BOM/LF/CRLF, shell direct-load integration, os.run/startup coverage, explicit unsupported routes | Entrypoint matrix backed by tests; no implicit language switch or contradictory runner header; PLANNED |
| M6 Host adapters and typed facade | Qualify required stock capability adapters; self/computer/Enum; type declarations; raw device/peripheral queries before helper methods | Runtime shapes and declarations match; capability/receiver/stale-result tests pass; PLANNED |
| M7 Turtle facade | Move/Turn/Inspect/Detect/GetFuel/GetInventory atop existing commands | Fuel/collision/protection/queue/partial failure/cancel tests; no behavior bypass; PLANNED |
| M8 Villager snapshots | Capability hardware/access rules, GetInfo/GetTrades dictionary, component enchantment data, optional FindTrades | Existing offers read without generation/mutation; exhaustion/price/permission/unload cases on both loaders; PLANNED |
| M9 Release qualification | Fork branding, native platform artifacts/hashes, dependency notices, source/build instructions, replacement install/rollback guide | Accurate compatibility claims and reviewed mixed-license combined distribution; PLANNED |

M1 is the **first implementation goal**. M2 design can proceed once baseline
contracts are understood; do not start host integration until M3 proves bounded
execution and safe cleanup. M6 scope comes from M1, not from copying Roblox APIs.

## M1 actionable work order

- Qualify JDK 25/Gradle 9.7.1/dependency resolution on the remote worker with cached,
  bounded builds. Preserve original versions. Record environmental failures apart
  from source regressions before changing dependencies.
- Build baseline core and both mod artifacts. Run :core:test (Java plus ROM),
  check excluding GameTests, then :fabric:runGametest and :forge:runGametest headlessly.
- Capture actual exported APIs under each device/configuration, including aliases,
  inherited native methods, returned handle methods, ROM modules and dynamic APIs.
- Expand ExistingApi.md into a contract/parity ledger using existing tests first;
  add tests only for meaningful gaps. Record inputs, result values/errors/events,
  suspension, resource limits, policy and hardware prerequisites.
- Prepare old-world/files fixtures and verify unchanged IDs, startup/disk precedence,
  stored programs, inventory/fuel and peripheral restoration. Keep user worlds out
  of experimental tests.
- Mark M1 complete only with passing evidence or explicitly bounded unsupported
  cases. Build success alone does not establish behavior/API coverage.

## Deferred decisions and features

Actual trading, automatic rerolls, pathfinding/MoveTo, concurrent Lua/Luau multishell,
cross-VM require/closures, a Luau BIOS, a new mod ID and broad native platform claims
are outside the initial scope. Each needs a separate decision and acceptance plan.
The VM can be developed/forked independently; choosing its license and linking it
to this mixed-license fork remain separate questions.
