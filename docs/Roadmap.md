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
| M2 Runtime design and repository boundary | Provisional generic repo name, official Luau primary candidate, ABI v1, session/host protocol, resource/fault model, M3 matrix and license analysis | **PARTIAL 2026-10-15 (static design):** contracts in Architecture/Runtime.md; no runtime proof, legal clearance or repo creation |
| M3 Standalone VM proof | Pinned Luau or justified alternative; isolated helper/synthetic host; ABI conformance, sandbox, compile/yield/resume, host requests, limits, stale completion, fatal containment and artifact provenance | **PLANNED:** Windows/Linux x64 executable proof, rejected unsafe inputs, callback races/OOM/crash/hang containment and **1,000 lifecycles per OS**; no Minecraft integration |
| M4 Opt-in developer runner | Managed child session, explicit luau command, yielded Cobalt caller, terminal ownership, event/host bridge, generation fencing | Returns/errors/terminate/reboot/unload work without BIOS corruption; Lua baseline green; both loaders qualified; PLANNED |
| M5 Program directives | First-line classification, BOM/LF/CRLF, shell direct-load integration, os.run/startup coverage, explicit unsupported routes | Entrypoint matrix backed by tests; no implicit language switch or contradictory runner header; PLANNED |
| M6 Host adapters and typed facade | Qualify required stock capability adapters; self/computer/Enum; type declarations; raw device/peripheral queries before helper methods | Runtime shapes and declarations match; capability/receiver/stale-result tests pass; PLANNED |
| M7 Turtle facade | Move/Turn/Inspect/Detect/GetFuel/GetInventory atop existing commands | Fuel/collision/protection/queue/partial failure/cancel tests; no behavior bypass; PLANNED |
| M8 Villager snapshots | Capability hardware/access rules, GetInfo/GetTrades dictionary, component enchantment data, optional FindTrades | Existing offers read without generation/mutation; exhaustion/price/permission/unload cases on both loaders; PLANNED |
| M9 Release qualification | Fork branding, native platform artifacts/hashes, dependency notices, source/build instructions, replacement install/rollback guide | Accurate compatibility claims and reviewed mixed-license combined distribution; PLANNED |

M1 is the first implementation baseline and **remains PARTIAL**; M2 now records
an independently reviewed static design, **not** a qualifying runtime pass.
Proceed to M3 standalone experiments only under an explicit work order. **Do not
start M4 host/Minecraft integration** until M3 proves bounded execution,
interrupted cleanup, cross-platform packaging and the chosen native fatal-fault
containment approach. M6 scope comes from M1, not from copying Roblox APIs.

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

## M2 decision and M3 entry gates (2026-10-15)

- Canonical design: [dual-VM runtime and ABI v1](Architecture/Runtime.md).
  Generic VM repository is provisionally **gmoddev/LuauRuntime**, not created.
  Official Roblox Luau is the primary evaluation backend, but its observed SHA
  is a research candidate, **not** a qualified or selected release dependency.
- M3 first freezes the exact Luau compiler+VM SHA and verifies Windows/Linux
  x64 ABI/layout, sandbox and continuation rules with a synthetic independent
  host. Hard loop/recursion interruption, compiler DoS, native allocation,
  cancellation while a callback is pending, stale completions and **1,000
  full session lifecycles on each OS** are mandatory evidence.
- Luau interrupt callbacks do not establish safe cooperative time-slicing or an
  exact instruction cap by themselves. Process/OS supervision is the preferred
  hard containment boundary. Fatal crash and callback blocking require their
  own isolated tests; Java exceptions do not isolate a native failure.
- M4 must separately demonstrate that pending stock main-thread tasks cannot
  mutate a new computer generation, Cobalt owns BIOS, the launcher yields and
  returns, and the single Luau terminal lease is revoked on every exit.
  Stock task completion events are named **task_complete** (singular).
- **Licensing gate:** preserve file-level CCPL/MPL and Luau MIT notices.
  Repository separation alone does not resolve CCPL §5's dependency condition.
  M9 release and native distribution require a documented legal review.
- These are planning/qualification requirements, not claims of implemented
  behavior. Preserve all M1 optional failures and open parity/restart gates.
