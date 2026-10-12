<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Upstream baseline

Verified from fetched Git source on 2026-10-12:

| Item | Value |
| --- | --- |
| Upstream | https://github.com/cc-tweaked/CC-Tweaked |
| Source branch | mc-26.3 |
| Commit | a95dbe739f99e47a399d120839177e77ac861896 |
| Fork | https://github.com/gmoddev/CCLuau |
| Development | main, derived from this commit |
| Baseline ref | baseline/mc-26.3, never advanced for features |
| Minecraft | 26.3 |
| Fabric API / Loader | 0.160.5+26.3 / 0.19.4 |
| NeoForge | 26.3.0.45-beta |
| Cobalt | strictly 0.9.9 |
| Java toolchain | 25 |
| Gradle wrapper | 9.7.1 |

Versions come from gradle/libs.versions.toml, gradle/gradle-daemon-jvm.properties,
gradle/wrapper/gradle-wrapper.properties and inherited CI. They are pinned source
configuration, not proof that every artifact resolves or builds. No dependency
versions were changed. A later baseline bump must record a new source SHA and
repeat loader/save qualification; do not silently change Minecraft versions.

The local upstream remote has pushing disabled. main tracks origin/main, not
upstream. Upstream history is preserved for provenance. Fork changes are never
offered to upstream for merging. GitHub Actions start disabled so copied workflows
do not run automatically before the fork's build policy is reviewed.
