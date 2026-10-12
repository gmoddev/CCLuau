<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# CCLuau agent instructions

CCLuau is an independent, AI-assisted CC: Tweaked fork for Minecraft 26.3. Work is
for this fork only. Never open upstream pull requests, request upstream review,
configure upstream merging, or push to cc-tweaked/CC-Tweaked. Fetching upstream
for comparison and importing qualified fixes into this fork is permitted.
AI-assisted contributions are welcome here; verify their behavior and provenance.

Read [AIContext.md](AIContext.md), [docs/Invariants.md](docs/Invariants.md), and
[docs/Roadmap.md](docs/Roadmap.md) before implementation. Update context and evidence
when a decision, integration boundary, or qualification status changes.

## Naming and observability

- Default to PascalCase for new identifiers, methods, variables, and public Luau
  fields. Use `GetFolder()` / `GetObj()`, never `GetOrCreateFolder()` / `GetOrCreateObj()`.
- `self = setmetatable({}, ...)` is the explicit local naming exception. The
  injected `self` and `computer` names are fixed proposed API names. Preserve
  inherited names, Java overrides, third-party API calls, and existing Lua public
  contracts exactly; do not rename stock `turtle.forward()` to enforce this style.
- Use `[System:SubSystem]` log prefixes, for example `[Runtime:Luau]` and
  `[Combat:MedicalSys]`. Do not mass-rewrite upstream logs.
- Expected failures return structured results or appear inside the computer's
  terminal/server logs. Development commands must capture failures in tool output.
  Never open modal error dialogs, steal focus, launch visible crash helpers, or
  overlay the user's game. A suspected native crash requires containment before
  game integration; exception handling cannot make an unsafe in-process VM safe.

## Implementation boundaries

- First milestone: establish the existing API and functionality, including
  executable baseline evidence, before implementing Luau or replacing APIs.
- Cobalt remains the default boot/BIOS and Lua runtime. Luau is a future explicit
  opt-in managed program session. Proposed APIs in documentation do not exist yet.
- Follow the numbered invariants. Host commands retain world authority; adapters
  preserve main-thread dispatch, limits, permissions, asynchronous results, and
  lifecycle. Never introduce direct world access from a VM worker.
- VM implementation and its generic native bridge belong in a separate repository.
  Do not copy CCPL files, signatures/documentation implementations, or game assets
  into it. The fork owns CC-specific adapters. See docs/Architecture/Runtime.md.
- Preserve every copyright, SPDX identifier, LICENSES entry, and REUSE annotation.
  AI policy text may be changed; license notices may not be stripped. Technical
  repository separation is not a license clearance claim.
- Prefer focused diffs. Use CodexLock/apply_patch when available. Do not rewrite
  inherited code solely for style. Do not delegate to subagents unless requested.
- Use the Gradle wrapper and source-defined tasks. Sustained builds/tests should
  use the configured remote-build-worker skill and bounded cached builds. Do not
  launch Minecraft clients unless explicitly requested. Headless tests come first.
- Report static review, unit tests, loader integration, live testing, and release
  review separately. Never mark a planned test or an upstream CI badge as a pass.

## Repository conventions

`main` is fork development rooted in mc-26.3. `baseline/mc-26.3` records the pinned
unmodified upstream commit. `upstream` is read-only; `origin` is gmoddev/CCLuau.
Fork pull requests target this fork's main only. No upstream contribution workflow.
Inherited GitHub Actions are initially disabled at repository level; intentional
fork build automation can be enabled after reviewing its tasks and credentials.
