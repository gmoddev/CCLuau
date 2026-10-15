<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Qualification ledger

Initial evidence date: 2026-10-12. M1 attempt: 2026-10-15. Source SHA is recorded
in UpstreamBaseline.md. **M1 is BLOCKED and is not qualified.**

| Evidence level | Status | Evidence / limitation |
| --- | --- | --- |
| Repository | Established | GitHub fork, main from exact mc-26.3 SHA, preserved history and baseline ref |
| Static architecture | Reviewed | Source map, entry paths, API registration, Cobalt lifecycle, queue guards, turtle commands and mixed-license examples |
| Static native API census | Established | 218 native declarations / 231 declaration-alias rows across 34 files; every annotation accounted for and source line verified; not runtime exports |
| Documentation checks | PASS | 13 new Markdown documents, 20 local links resolved; census regeneration check and git diff --check pass; runtime/build/license files unchanged |
| Core compile / Java + ROM tests | BLOCKED | Two wrapper invocations stop before compilation because JDK 25 is absent and daemon provisioning has no Windows x64 URL; zero tests executed |
| Fabric / NeoForge builds | BLOCKED | Shared JDK prerequisite prevents configuration; neither loader build was run |
| Headless GameTests | BLOCKED | Same prerequisite; neither loader's GameTests were run |
| Live game/save migration | BLOCKED | No full save/reload evidence; no game window launched or user world altered |
| Native runtime | NOT IMPLEMENTED | Separate-repository backend qualification is future M2/M3 work |
| Release qualification | NOT CLEARED | No native/binary release; no combined license conclusion |

Use the existing source-defined Gradle wrapper tasks. Planned downstream commands,
to run on the configured remote worker once Java 25 is available:

```text
gradlew.bat --no-daemon --max-workers=2 --configure-on-demand :core:assemble :core:test
gradlew.bat --no-daemon --max-workers=2 :fabric:assemble :forge:assemble
gradlew.bat --no-daemon --max-workers=2 check -x runGametest
gradlew.bat --no-daemon --max-workers=2 :fabric:runGametest :forge:runGametest
```

Except for the first core command (attempted below), these are plans, not executed checks.
Check task availability during configuration;
do not assume a dependency download or toolchain failure is a mod code regression.

Each future entry records source/VM SHAs, host OS/architecture, Java/Gradle versions,
loader/config/fixture hashes, exact command, worker count, exit status, reports and
artifact hashes. Add failure/reproduction details rather than replacing NOT RUN
with an unexplained PASS. A standalone test never substitutes for loader evidence.

## M1 execution record — 2026-10-15

Source under test: `e0c7bf84aba7a506a4fe2aa243c4b39eb319518b` for the initial stock
attempt. The second attempt used that revision plus the uncommitted test/runner
files listed in its metadata. Neither reached source compilation, so neither is
evidence that the new tests compile. Dependencies and main production sources
were not changed to work around the blocker.

Worker: SSH alias dockerbox, host HOSTPC, Windows 11 Pro 10.0.26200 AMD64,
24 logical processors, 34,282,344,448 bytes RAM; approximately 17.2 GiB free at
the environment capture. Existing Java 17 and 21; default Oracle Java
21.0.8+12-LTS-250. Source requires Java 25. Wrapper Gradle 9.7.1 downloaded and
started successfully. All build attempts used two workers and a headless JVM.

Prepared probes/tooling are committed at `70a3f7444`; they have not compiled or
executed. [Manifest.json](evidence/M1-20261015/Manifest.json) records full source
commit and SHA-256 hashes for the prepared files and captured evidence. Original
PowerShell UTF-16/BOM text was losslessly transcoded to UTF-8 for readable diffs.

Persistent paths (all retained for incremental retries):

- Workspace/build outputs: `C:\Sandbox\Codex\Workspaces\CCLuau` and its project build directories.
- Gradle cache: `C:\Sandbox\Codex\Cache\CCLuau\Gradle`.
- Logs: `C:\Sandbox\Codex\Logs\CCLuau\M1-20261015`.
- No mod artifacts, runtime inventory output, or test XML were produced.
- No build process or Minecraft client remains running from these attempts.

| Executed command | Exit/result | Time |
| --- | --- | --- |
| gradlew.bat --no-daemon --max-workers=2 --configure-on-demand :core:assemble :core:test | 1; BLOCKED before compilation | 25.8383 s |
| powershell -NoProfile -NonInteractive -ExecutionPolicy Bypass -File C:\Sandbox\Codex\Workspaces\CCLuau\tools\RunBaseline.ps1 -Stage Core -TimeoutMinutes 2 | 1; BLOCKED; invokes wrapper with --no-daemon --max-workers=2 --console=plain --configure-on-demand :core:assemble :core:test | 1.0495 s |
| python tools/TestRuntimeInventory.py | 0; PASS, 1 synthetic-data unittest / 4 subtests | 0.001 s reported by unittest |
| python tools/InventoryApis.py --check | 0; PASS, existing 231 declaration/alias rows unchanged | Not timed |
| PowerShell Language.Parser.ParseFile on tools/RunBaseline.ps1 | PASS, no syntax errors | Not timed |
| git diff --check | 0; PASS | Not timed |

The second wrapper attempt validates the new runner's bounded execution and log
capture; it is not a second independent runtime result. The local tools checks
are low-impact checks, not an alternative local Minecraft build.

Observed Gradle error: "No defined toolchain download url for WINDOWS on x86_64
architecture" for languageVersion=25. This is an infrastructure/toolchain blocker,
not an observed source, Java test, ROM, loader, or game regression. Do not lower
the Java target or Minecraft/dependency versions to conceal it. An official
portable JDK 25 under the Codex tools directory is a proposed remedy; installation
requires owner approval under the remote worker skill. No toolchain was installed.

Raw evidence: [environment](evidence/M1-20261015/Environment.json),
[initial command metadata](evidence/M1-20261015/01-CoreBaseline.json),
[initial combined output](evidence/M1-20261015/01-CoreBaseline.log),
[runner metadata](evidence/M1-20261015/20261015T072645061Z-Core.json),
[runner stdout](evidence/M1-20261015/20261015T072645061Z-Core.stdout.log),
[runner stderr](evidence/M1-20261015/20261015T072645061Z-Core.stderr.log), and
[local tooling checks](evidence/M1-20261015/LocalChecks.json).

## Area-by-area qualification

| Area | Status | Prepared executable coverage / remaining limit |
| --- | --- | --- |
| Remote wrapper/bootstrap | PARTIAL | Pinned Gradle downloaded and starts; JDK 25 provisioning blocks project configuration |
| Runtime API registration/exports | BLOCKED | BaselineTest captures booted core globals/methods; comparator checks existing core census names; no output yet; loader/device/handle exports still need coverage |
| BIOS and shell/os.run | BLOCKED | New real-BIOS test plus existing shell_spec.lua; argument packing, environment and success/error cases prepared, not executed |
| Events/filtering/termination | BLOCKED | New queued-event/nil-arity and terminate-vs-raw tests plus existing os_spec.lua; not executed |
| Main-thread asynchronous calls | BLOCKED | New executeMainThreadTask and issueMainThreadTask probes check thread and results; not executed; stale completion across reboot/unload remains a gap |
| Reboot/unload and cleanup | BLOCKED | New lifecycle hook counts and bounded worker close; not executed; does not prove all handles/HTTP/peripherals release |
| Turtle movement | BLOCKED | Existing Move_preserves_state, Move_obstruct, Move_water, Move_push_entity and refuel GameTests queued for execution on both loaders |
| Turtle queue | BLOCKED | New Baseline_queue fixture checks 17 accepted pending commands, next rejected, FIFO and no inventory/fuel changes; not executed |
| Core filesystem/startup persistence | BLOCKED | New JUnit temporary-directory fixture boots two fresh hosts and verifies startup counter/filesystem and configured ID; not executed |
| Minecraft persisted device state | PARTIAL | Dedicated serialized turtle fixture established (ID 31, fuel 80, slot 0, 32 dirt, label); existing movement fixture retained; no loader execution or full world save/reload, so runtime compatibility remains unverified |
| Qualification tools | PASS | Runner syntax, missing-method/API and empty-census rejection tests, and source census reproducibility checks passed; synthetic checks are not game evidence |

The test-only Checkstyle suppression is limited to BaselineTest's identifier
naming because the owner's PascalCase policy conflicts with inherited Java naming
rules. Existing production style rules remain intact. REUSE adds an annotation
for factual evidence files; no upstream notices or licenses were removed.

## Resume and M2 prerequisites

1. Supply an existing JDK 25 or approve an isolated portable JDK on dockerbox.
   Use RunBaseline.ps1 -JavaHome with the actual installation path; preserve the
   Gradle cache and source configuration. Record full JDK build and archive hash.
2. Execute Core first, resolving any diagnosed test/build issues. Then execute
   Loaders, Checks and GameTests stages sequentially. Each stage has a 30-minute
   default bound, two workers and separate stdout/stderr/JSON. Inspect dependency
   resolution and test XML before assigning PASS; a successful wrapper alone is
   insufficient. Inventory comparison requires the emitted runtime JSON.
3. Finish real loader/device API inventories and full isolated world-save/reload
   coverage: computer IDs/labels/power state, filesystem and disk/root startup
   precedence, turtle selected slot/inventory/fuel/upgrades, unload and restart.
4. Close execution-critical gaps affecting M2-M4: pending host callbacks at reboot,
   event pressure, returned handle cleanup, terminal redirection/multishell scope,
   queued turtle operations during unload and device capability availability.
5. Reclassify M1 only from passing core and both-loader evidence with explicit
   bounded exceptions. M2 implementation has not begun and must not start
   automatically; use the qualified contracts to inform a separately authorized
   runtime design decision. M3 still requires standalone native safety evidence
   before any M4 host integration.
