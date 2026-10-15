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
| Official Luau evaluation | [Official upstream MIT source](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/LICENSE.txt) | MIT notice attributes Roblox Corporation and Lua.org; research SHA is not a production pin; preserve exact upstream license and transitive notices |

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

## M2 combined-distribution review (2026-10-15)

**Status: legal clearance NOT GRANTED.** CCLuau is a mixed-file-license
fork, not a wholly MPL or permissively relicensed project. Its
[CCPL text](../LICENSES/LicenseRef-CCPL.txt) defines a dependency broadly and
in §5 requires dependent mods/classes to have terms comparable to CCPL, with
exceptions for Minecraft and the mod loader. §5 also discusses source
availability for binary redistribution. §7 governs use of CCPL code/assets
in other projects and contains non-commercial restrictions. Whether any
specific independently authored Luau runtime, its license, and chosen mode
of linking or packaging meet these provisions needs competent legal analysis;
architecture cannot supply that legal determination.

| Distribution arrangement | Technical treatment | Licensing conclusion |
| --- | --- | --- |
| Independent generic VM source repository (proposed gmoddev/LuauRuntime) | No CC classes, CCPL interfaces, ROM, namespaced signatures, or assets copied; original files may be MIT, preserving MIT Luau attribution | Independently authored provenance is feasible; **does not clear** combined dependency distribution |
| Static Luau linkage into an adapter packaged with CCLuau | Native runtime/compiler and Java/CC adapters ship together | Requires CCPL §5, MPL file-level, MIT and other third-party inventory/legal review |
| Dynamic bundled DLL/SO in the mod | Separate native binary loaded by the same JVM/process | A separate binary/shared library is **not** an automatic CCPL dependency exception |
| Supervised companion process or independently installed runtime | IPC isolates crashes and may simplify separate licenses/notices | Process boundary is **not** a verified legal exemption; distribution and dependency relationship still reviewed |
| Runtime optional download/installer | Installer or packaging may fetch an exact pinned artifact | Not a basis to evade notice, source, dependency, security or distribution requirements |
| Standalone generic-runtime tests and synthetic host | No CCLuau source, binaries or assets distributed with the generic runtime | Can be developed on its own provenance; review all actual third-party components |

**M2 repository plan:** choose MIT for entirely new, independent generic VM
wrapper/test code after owner approval; import Luau under its original MIT
notices and retain Lua-origin notice as applicable. Prefer upstream source as a
pinned dependency/submodule or vendored snapshot with full provenance and
verification. Record selected Git SHA, complete build/toolchain commands,
compiler flags, upstream LICENSE.txt, any third-party or test dependencies,
ABI/public export inventory, binary SHA-256 and SBOM. Do not describe the
upstream research observation 8387cfb461b38ce09e37c1e4c2811538ef1bf5cb
as a qualified dependency until M3 builds and validates it.

**M9 gates, regardless of process model:**

1. Audit inherited source/ROM/assets by actual per-file license/REUSE mapping;
   retain CCPL and MPL headers; document which new CCLuau bridge files are
   original MPL and which contain upstream-derived sections.
2. Review CCPL §§5 and 7, actual license compatibilities, the Luau MIT wrapper,
   and direct/transitive runtime dependencies for the precise proposed
   linked/packaged/downloaded release. Obtain affirmative legal clearance
   before native or commercial distribution; no blanket assertion that
   MIT and CCPL are comparable or incompatible.
3. Build complete source-correspondence instructions, dependency SBOM, required
   notices and attribution, reproducible native manifest, hashes and user-visible
   source access. Qualify Minecraft mod branding and replacement-install policy.
4. Keep release disabled until M3/M4/loader safety and mixed-license legal review
   are recorded separately. A design-only M2 approval is not a binary release.

Specific sources: [Luau README/build instructions](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/README.md),
[Luau MIT license](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/LICENSE.txt),
[official Luau build configuration](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/CMakeLists.txt),
this fork's [REUSE file](../REUSE.toml) and [CCPL license](../LICENSES/LicenseRef-CCPL.txt).
