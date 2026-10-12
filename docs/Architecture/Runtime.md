<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Separate VM architecture

The VM and generic native bridge will live in a separate repository. Its name,
license, revision and backend have not been selected; no second repository or VM
implementation has been created in this initialization task.

| Separate VM repository | This CCLuau fork |
| --- | --- |
| Independently written generic ABI, VM creation, compilation, resume/yield, cancellation, allocation accounting, sandbox, values and errors | CC-specific program launcher, session manager, event dispatch, terminal/filesystem/peripheral adapters, turtle commands and world services |
| Official Luau fork or dependency as an initial feasibility candidate, pinned compiler/VM versions and retained notices | Continue using Cobalt and existing ILuaMachine for BIOS/legacy Lua |
| Standalone tests with synthetic host requests; no CC classes, copied CCPL source or Minecraft assets | ComputerContext/ComputerExecutor integration and both loader qualification |
| Reproducible native artifacts, platform manifest, versioned generic interface | Optional artifact loading and explicit Luau-unavailable program error |

Start with the official Luau compiler/VM rather than committing to a new language
implementation before measuring feasibility. A custom/forked VM remains possible
if callback suspension, watchdog behavior, memory accounting or packaging cannot
meet requirements. Record the reason and evidence before selecting another backend.

## Proposed host contract

Use an independently authored, versioned interface expressing CreateSession,
CompileSource, Resume, RequestCancel, GetMetrics and CloseSession. Names are design
vocabulary, not final JNI signatures. Host calls use request IDs, bounded copied
values, and opaque capability tokens. Native state handles are generation tagged;
never expose pointers or Java objects to a program.

Sessions progress Created -> Compiled -> Runnable -> WaitingEvent/WaitingHost ->
Completed/Failed/Cancelled -> Closed. Close must remain idempotent. The host fences
results by (ComputerId, BootGeneration, SessionId). Execution belongs on supervised
computer workers; world requests queue to the main thread and suspend the program.
Prove Luau native callback/yield restrictions before embedding this design.

Initially keep JIT disabled, reject supplied bytecode, protect built-ins, use
per-session environments, and enforce allocator/interrupt limits. Long-running
host/native calls need their own bounds: the VM interrupt cannot prove that a
blocking C callback is safe. No crashing prototype runs in the user's game.

## Qualification before integration

Require Windows/Linux x64 compile/run, syntax/runtime errors, event waits, async
host calls, infinite-loop interruption, deep recursion, table cycles/huge values,
out-of-memory handling, cancellation during callbacks, 1000 create/close cycles,
thread affinity and allocation cleanup. Then qualify a developer runner in the
fork, preserving Cobalt and releasing terminal ownership on every exit.

Repository separation prevents accidental copying and supports reuse. It does
not determine the licensing of the CC-specific adapter or combined distribution.
See [LicenseInventory.md](../LicenseInventory.md). No binary/native distribution
is authorized by a documentation milestone alone.
