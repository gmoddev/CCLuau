<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Qualification ledger

Initial evidence date: 2026-10-12. M1 attempt: 2026-10-15. Source SHA is recorded
in UpstreamBaseline.md. **M1 is PARTIAL and is not fully qualified.** Builds, core
checks and the required Windows x64 headless cases pass. Unchanged optional stock
GameTests fail, and broader coverage limits remain explicit below.
The owner approved portable JDK 25 provisioning after the initial blocked attempt.

| Evidence level | Status | Evidence / limitation |
| --- | --- | --- |
| Repository | Established | GitHub fork, main from exact mc-26.3 SHA, preserved history and baseline ref |
| Static architecture | Reviewed | Source map, entry paths, API registration, Cobalt lifecycle, queue guards, turtle commands and mixed-license examples |
| Static native API census | Established | 218 native declarations / 231 declaration-alias rows across 34 files; every annotation accounted for and source line verified; not runtime exports |
| M0 documentation checks | PASS | Original 13 Markdown documents/20 links were validated; M1 extends this documentation and retains original licenses |
| Core compile / Java + ROM tests | PASS | Approved isolated JDK 25 resolves the initial blocker; full suite: 1644 tests, 0 failures/errors, 15 skips; five focused probes pass |
| Fabric / NeoForge builds | PASS | Both pinned 26.3 loader assemble tasks pass under the approved portable JDK; jars and source jars retained with SHA-256 hashes |
| Required headless GameTests | PASS | 113 required cases pass per loader; all new baseline probes pass |
| Complete headless GameTest suites | PARTIAL | Fabric: 114 passes/2 optional failures; NeoForge: 113/3; reporter encodes optional failures as skipped and Gradle exits 0 |
| Non-GameTest repository checks | PASS | 1719 tests: 1704 passed, 15 skipped; all configured checks pass on final source |
| Save/persistence fixtures | PASS | Fresh-host filesystem/startup, mounted-handle closure, and real NBT disk/fresh-entity round trip on both loaders |
| Full world restart/client migration | PARTIAL | No complete server/world restart migration or interactive client test; no user world altered |
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

At that point, prepared probes/tooling were committed at `70a3f7444` and had not
compiled or executed. [Manifest.json](evidence/M1-20261015/Manifest.json) records full source
commit and SHA-256 hashes for the prepared files and captured evidence. Copied
PowerShell text was transcoded to UTF-8 and trailing whitespace normalized for
readable diffs. Original bytes remain on the worker; their hashes are recorded
in [RawRemoteHashes.json](evidence/M1-20261015/RawRemoteHashes.json).

Persistent paths (all retained for incremental retries):

- Workspace/build outputs: `C:\Sandbox\Codex\Workspaces\CCLuau` and its project build directories.
- Gradle cache: `C:\Sandbox\Codex\Cache\CCLuau\Gradle`.
- Logs: `C:\Sandbox\Codex\Logs\CCLuau\M1-20261015`.
- These initial blocked attempts produced no mod artifacts, runtime inventory output, or test XML.
- No build process or Minecraft client remained running from these initial attempts.

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
portable JDK 25 was proposed at that point and awaited owner approval. The owner
subsequently approved it; the approved-JDK execution record below supersedes this blocker.

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
| Remote wrapper/bootstrap | PASS | Approved, isolated, checksum-verified Temurin 25.0.4.1+1 with Gradle 9.7.1; two workers, persistent caches |
| Runtime core/turtle exports | PASS | Core and both-loader normal/advanced/turtle profiles match 82 native core names and 44 turtle names; no invented APIs |
| Broader API parity | PARTIAL | Pocket/command profiles, constants, all returned handle shapes, addon registrations and full peripheral matrices are not captured |
| BIOS and shell/os.run | PASS | Real BIOS boot, require, arguments, supplied environment, success/error cases and stock ROM suites |
| Events/filtering/termination | PASS | Filtered events, nil arity, terminate bypass and raw terminate; actual host event spelling pinned as task_complete |
| Main-thread asynchronous calls | PASS | executeMainThreadTask/issueMainThreadTask thread and completion values verified; stale callback races remain outside this pass |
| Reboot/unload and filesystem cleanup | PASS | Hook counts, bounded worker close, fresh boot, and deliberately unclosed mounted-channel cleanup pass |
| Wider resource lifecycle/races | PARTIAL | Pending callbacks across reboot, all HTTP/peripheral handles, and unload under event pressure remain unqualified |
| Turtle movement | PASS | Existing state-preserving, obstructed, water/entity movement and refuel GameTests pass on both loaders |
| Turtle queue | PASS | Existing 17-command acceptance boundary, next rejected, FIFO order and unchanged inventory/fuel pass on both loaders |
| Core filesystem/startup persistence | PASS | Two fresh hosts over an isolated on-disk mount preserve startup counter/filesystem; configured computer identity checked |
| Minecraft persisted device state | PASS | ID 31, label, fuel 80, 32 dirt, selected slot 5, capacity and power flag survive actual NBT disk/fresh-entity round trip on both loaders |
| Full server/world restart | PARTIAL | Block serialization plus fresh core hosts are not proof of complete world migration or disk/root startup precedence |
| Optional stock game behaviors | PARTIAL | Treasure-disk loot and bucket reach tests fail on both loaders; brewing-stand item limits fail on NeoForge; source bodies unchanged from baseline |
| Qualification tools | PASS | Runner syntax, missing-method/API and empty-census rejection tests, and source census reproducibility checks passed; synthetic checks are not game evidence |

The test-only Checkstyle suppression is limited to BaselineTest's identifier
naming because the owner's PascalCase policy conflicts with inherited Java naming
rules. Existing production style rules remain intact. REUSE adds an annotation
for factual evidence files; no upstream notices or licenses were removed.

## Approved-JDK execution and results

The owner approved the portable JDK on 2026-10-15. No system Java or PATH setting
changed. [Jdk25.json](evidence/M1-20261015/Jdk25.json) records the official archive,
installation path, and verified SHA-256
`00c847d804f4a78e9f04f2683faf14fed898535b177b7fc704486cb0284e9283`.
JavaHome is `C:\Sandbox\Codex\Tools\CCLuau\Temurin25\jdk-25.0.4.1+1`.
The earlier missing-toolchain blocker is resolved.

Executable test/tool changes are committed at `f5747ddd1`. The Gradle runs used
`b334f15d7` plus the source changes listed in [TestedSource.json](evidence/M1-20261015/TestedSource.json).
All nine listed test/runner inputs match the final committed sources byte-for-byte.
The additional `.fabric/processedMods` jar in that raw record is generated cache
output, not source; a narrow gitignore entry now keeps it out of source snapshots.
[ConfigurationsAndFixtures.json](evidence/M1-20261015/ConfigurationsAndFixtures.json)
records the two loader configuration hashes and seven relevant structure hashes.
[ExecutionManifest.json](evidence/M1-20261015/ExecutionManifest.json) binds tested
inputs, analysis tools, counts and evidence hashes to the source commit.
[ApprovedRunRawHashes.json](evidence/M1-20261015/ApprovedRunRawHashes.json) retains
hashes of original worker logs/metadata; copied metadata is normalized UTF-8 JSON.
Repository evidence uses LF endings so its manifest hashes survive checkout on
Windows and other platforms. The original worker byte hashes remain separate.

Every stage below was invoked through `tools/RunBaseline.ps1 -Stage <Stage>
-JavaHome <JavaHome> -TimeoutMinutes 30`, except focused diagnostics, which used
10 minutes. The wrapper command prefix is exactly
`gradlew.bat --no-daemon --max-workers=2 --console=plain`. Metadata files include
full commands, source/dirty state, timings, stdout/stderr paths and artifact roots.

| Stage and wrapper task arguments | Exit / result | Elapsed | Metadata |
| --- | --- | --- | --- |
| Core --configure-on-demand :core:assemble :core:test (initial approved run) | 1; only the new event probe failed | 333.5821 s | [073546](evidence/M1-20261015/20261015T073546571Z-Core.json) |
| Focused --configure-on-demand :core:test --tests dan200.computercraft.core.computer.BaselineTest (diagnostic) | 1; 4/5 pass, stage markers isolate wrong event name | 31.9847 s | [074152](evidence/M1-20261015/20261015T074152180Z-Focused.json) |
| Focused, same arguments after correction | 0; 5/5 pass | 20.4939 s | [074304](evidence/M1-20261015/20261015T074304893Z-Focused.json) |
| Core --configure-on-demand :core:assemble :core:test | 0; 1644 tests, 0 failures/errors, 15 skips | 102.6753 s | [074351](evidence/M1-20261015/20261015T074351550Z-Core.json) |
| Loaders :fabric:assemble :forge:assemble | 0; both loaders and source jars built | 217.6035 s | [074552](evidence/M1-20261015/20261015T074552014Z-Loaders.json) |
| Checks check -x runGametest (initial) | 1; new Kotlin test type arguments and PascalCase lint | 105.2854 s | [075046](evidence/M1-20261015/20261015T075046549Z-Checks.json) |
| Checks check -x runGametest (corrected) | 0; 1719 tests, 0 failures/errors, 15 skips | 68.6421 s | [075336](evidence/M1-20261015/20261015T075336581Z-Checks.json) |
| GameTests :fabric:runGametest :forge:runGametest (initial) | 1; new queue wait caused one required failure; optional failures also present; NeoForge not reached | 64.7048 s | [075621](evidence/M1-20261015/20261015T075621460Z-GameTests.json) |
| GameTests, same arguments after correction | 0; no required failures; Fabric 114 passes/2 optional failures and NeoForge 113/3 | 57.6983 s | [075753](evidence/M1-20261015/20261015T075753787Z-GameTests.json) |
| Checks check -x runGametest (final source) | 0; final queue-test change passes configured checks | 18.6717 s | [075954](evidence/M1-20261015/20261015T075954183Z-Checks.json) |

The failed probes were corrected without modifying production execution semantics:
the inherited Javadoc says task_completed, while LuaContext/TaskCallback actually
use task_complete; Kotlin required explicit generic types and a method-local
PascalCase naming suppression; GameTest waits require a retryable framework
assertion rather than an ordinary JUnit exception. [EventProbeDiagnostic.xml](evidence/M1-20261015/EventProbeDiagnostic.xml)
retains the localized event failure. Raw console logs for every attempt remain
at the metadata's worker paths. No required-test failure remains observed;
optional stock-test failures are recorded below rather than treated as passes.

[CoreSuiteSummary.json](evidence/M1-20261015/CoreSuiteSummary.json) records all core
suite counts and skipped names. [ChecksSuiteSummary.json](evidence/M1-20261015/ChecksSuiteSummary.json)
contains core 1644, common 47, Fabric 11, NeoForge 11 and lints 6 tests. Of 1719
tests, 1704 pass and 15 are skipped. The skips cover existing GPS/random-location,
JSON edge cases, read-only mounts and latest-file-size cases; none is promoted to
PASS. [CoreBaselineTest.xml](evidence/M1-20261015/CoreBaselineTest.xml) records the
five new core probes. All six loader runtime profiles match their selected
native method census; normal/turtle terminals report monochrome and advanced
computers report color as expected.

[GameSuiteSummary.json](evidence/M1-20261015/GameSuiteSummary.json) lists every
GameTest, with raw [Fabric XML](evidence/M1-20261015/Fabric/GameTests.xml) and
[NeoForge XML](evidence/M1-20261015/NeoForge/GameTests.xml). The new inventory test
uses real Cobalt ID-0 devices. Many existing turtle command tests deliberately use
ManagedComputers' Kotlin VM, so those tests prove host/command behavior, not full
Lua-to-world scheduling under production timing. The GameTest server also waits
for computer idleness to improve determinism. Race behavior needs separate proof.

### Optional failures and reporter semantics

`JunitTestReporter.onTestFailed` writes a `failure` node for required tests and a
`skipped` node for optional tests. These optional cases **ran and failed**; they
are not successful tests or ordinary unexecuted skips. There are three optional
definitions in the source, so each loader's 113 required cases pass. Audit with:

```text
python tools/SummarizeTests.py docs/evidence/M1-20261015/Fabric/GameTests.xml docs/evidence/M1-20261015/NeoForge/GameTests.xml --gametest
```

The audit returns exit 1 and PARTIAL for these reports even though Gradle exits 0.
[GameTestAudit.json](evidence/M1-20261015/GameTestAudit.json) records exact counts
and messages; [OptionalFailureProvenance.json](evidence/M1-20261015/OptionalFailureProvenance.json)
verifies the three test bodies are unchanged from the pinned upstream source.
This is not a claim that an independent pristine-upstream run was performed.

| Optional test | Fabric | NeoForge | Observed limit / source evidence |
| --- | --- | --- | --- |
| loot_test.chest_contains_disk | Failed | Failed | Expected treasure disk absent from fixed-seed dungeon loot; existing source FIXME questions datapack injection. Root cause is not proven here. |
| turtle_test.place_use_reach_limit | Failed | Failed | Bucket placement returns false / Cannot place item here; existing source FIXME already records unexplained behavior since 1.21.4. Reach behavior is unqualified. |
| inventory_test.brewing_stand_item_limit | Passed | Failed | NeoForge returns 0L instead of expected slot limit 1; existing optional test references issue 2480. Loader-specific limit semantics need investigation. |

No assertion, required flag, or production implementation was weakened to remove
these failures. They are unresolved behavior/fixture limitations and prevent a
fully green M1 qualification. The required lifecycle, movement, queue, inventory
capture and persistence probes still pass in their tested scope. The strict
report-audit tool has synthetic tests proving that optional failures cannot be
silently promoted to PASS, and empty reports cannot pass.

Local tooling validation passes two unittests with eight synthetic-data subtests
(`python tools/TestRuntimeInventory.py`), the unchanged 231-row native census
check, and the six real loader export comparisons. The strict GameTest audit's
exit 1 is an expected PARTIAL classification, not a tooling crash. Only data
copies and static/report checks run on the controlling PC; sustained builds and
Minecraft execution remained on dockerbox.

[BuiltJars.json](evidence/M1-20261015/BuiltJars.json) records retained binary/source
jar paths, sizes and SHA-256 hashes. Primary binary hashes:

- Fabric: `41bdbedd97671236d53c73d17fda258e26b2704bab357853fc33fababe7efb70`.
- NeoForge: `2c7989c07ee37a1e20daee4674569caae3ee4ee7c4ee16718b7520ff085d0c5b`.

Artifacts are under `C:\Sandbox\Codex\Artifacts\CCLuau\M1-20261015`; source,
incremental build outputs, downloaded dependencies and the Gradle cache are
retained. Exact environments/commands are reproducible; byte-for-byte clean
rebuild reproducibility and cross-platform execution were not tested. Compiler
deprecation/classfile warnings remain in inherited code/dependencies. No build or
game process remains running; no interactive Minecraft client was launched.

## M2 prerequisites and limits

M1's required execution-critical baseline passes, but overall M1 remains PARTIAL;
the implementation of M2 has not begun. Resolve the optional failures or explicitly
approve a reduced qualification scope before promoting M1 to fully qualified.
Further runtime design should use task_complete and the actual program-entry
contracts verified here. Before M2 implementation, explicitly decide the intended
API/device compatibility scope and separate VM repository/backend/ABI ownership.

Before M4 integration, close the material remaining gaps: stale main-thread
results at reboot/unload; event/command pressure and cancellation; all returned
handle/peripheral/HTTP resource lifecycles; terminal redirection/multishell
ownership; pocket/command profiles; disk-vs-root startup precedence; upgrade
state and full isolated server/world restart migration. The current persistence
probes prove on-disk core filesystem continuity and NBT disk/fresh-entity round
trips, not a complete world restart. Keep the 15 skipped cases explicit. M3 still
requires standalone native interruption, allocator, marshalling and lifecycle
qualification before any native backend is integrated. Do not start M2 automatically.
