<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# License provenance and repository boundary

Initial verified examples, not a complete legal/SBOM audit. Preserve upstream
file-specific notices, LICENSES/ and REUSE.toml. Removing the upstream contribution
policy's AI rejection does not remove copyright or licensing conditions.

| Material | Verified source | Handling |
| --- | --- | --- |
| ILuaMachine and ILuaContext | Individual headers: LicenseRef-CCPL | Retain notices and terms; do not copy into generic VM repository |
| RedstoneMethods and original-derived material | Individual CCPL headers / REUSE annotations | No blanket relicensing or notice deletion |
| ComputerContext, MachineEnvironment, many newer files | Individual MPL-2.0 headers | Preserve MPL and modified-file provenance |
| Original assets/selected ROM | REUSE.toml CCPL annotations, sidecars/headers | Keep assets in fork, preserve attribution |
| Other upstream material | LICENSES/, REUSE.toml, file headers | Includes CC0, CC-BY variants, MIT/Apache; complete per-file review later |
| New standalone fork documentation/tooling | Explicit MPL-2.0 headers | New authored material only; does not relicense upstream mod |
| Generated native API declaration census | Mixed-license sidecar and per-row SourceLicense | Source signatures retain provenance; not a license change to contributing files |
| Cobalt | Existing catalog dependency, version 0.9.9 | Artifact/transitive notices still need release inventory |
| Future Luau/backend | Not included | Pin revision and review upstream VM/dependency notices when selected |

CCPL section 5 imposes source/distribution terms and a comparable-conditions
dependency provision. A separate VM repository supports independent provenance
but does not remove that provision from a distribution depending on the VM.
No claim that repo separation "avoids CCPL" for the combined product is made.

Before a release, generate complete file-level SPDX/REUSE coverage and a dependency
SBOM, include corresponding modified source/build instructions, preserve all
third-party notices, and resolve the combined-runtime dependency interpretation.
This foundation publishes fork source under retained existing terms; it provides
no new clearance for native/binary/commercial distributions.

Primary evidence: [local CCPL text](../LICENSES/LicenseRef-CCPL.txt),
[REUSE annotations](../REUSE.toml), and
[upstream CCPL source](https://github.com/cc-tweaked/CC-Tweaked/blob/mc-26.3/LICENSES/LicenseRef-CCPL.txt).
