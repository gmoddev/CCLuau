<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Qualification ledger

Initial evidence date: 2026-10-12. Source SHA is recorded in UpstreamBaseline.md.

| Evidence level | Status | Evidence / limitation |
| --- | --- | --- |
| Repository | Established | GitHub fork, main from exact mc-26.3 SHA, preserved history and baseline ref |
| Static architecture | Reviewed | Source map, entry paths, API registration, Cobalt lifecycle, queue guards, turtle commands and mixed-license examples |
| Static native API census | Established | 218 native declarations / 231 declaration-alias rows across 34 files; every annotation accounted for and source line verified; not runtime exports |
| Documentation checks | PASS | 13 new Markdown documents, 20 local links resolved; census regeneration check and git diff --check pass; runtime/build/license files unchanged |
| Core compile / Java + ROM tests | NOT RUN | Required in M1; no binaries generated in this documentation setup |
| Fabric / NeoForge builds | NOT RUN | Dependency catalog read, artifact resolution unverified |
| Headless GameTests | NOT RUN | Required M1 loader and later feature gates |
| Live game/save migration | NOT RUN | No game window launched or user world altered |
| Native runtime | NOT IMPLEMENTED | Separate-repository backend qualification is future M2/M3 work |
| Release qualification | NOT CLEARED | No native/binary release; no combined license conclusion |

Use the existing source-defined Gradle wrapper tasks. Candidate M1 commands, to
run on the configured remote worker with appropriate bounded options:

```text
gradlew.bat --no-daemon --max-workers=2 --configure-on-demand :core:assemble :core:test
gradlew.bat --no-daemon --max-workers=2 :fabric:assemble :forge:assemble
gradlew.bat --no-daemon --max-workers=2 check -x runGametest
gradlew.bat --no-daemon --max-workers=2 :fabric:runGametest :forge:runGametest
```

These are plans, not executed checks. Check task availability during configuration;
do not assume a dependency download or toolchain failure is a mod code regression.

Each future entry records source/VM SHAs, host OS/architecture, Java/Gradle versions,
loader/config/fixture hashes, exact command, worker count, exit status, reports and
artifact hashes. Add failure/reproduction details rather than replacing NOT RUN
with an unexplained PASS. A standalone test never substitutes for loader evidence.
