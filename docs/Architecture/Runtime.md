<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# M2 decision record — dual VM runtime and generic native ABI

**Status: M2 PARTIAL (2026-10-15). Architecture selected for M3 experiments; no VM
built, no Minecraft code changed, no release or legal clearance.** The source
baseline is CCLuau branch m1-baseline-qualification at
1560215e5b66d1d7efebcba4bd14651856f48196. M1 remains PARTIAL. Its required
runtime baselines pass; the optional GameTest failures, stale-callback race,
interactive client, full world restart and peripheral/device parity gaps remain
open. Do not infer M3 or M4 readiness from this design.

This document is the canonical runtime design; do not duplicate it in a second
architecture file. See [ProgramEntry.md](ProgramEntry.md) for loader routes,
[CodeMap.md](CodeMap.md) for CCLuau ownership, [Invariants.md](../Invariants.md)
and [Qualification.md](../Qualification.md) for evidence and gates.

## D1 — Backend and independent repository

**Recommendation: gmoddev/LuauRuntime**, provisionally named (not created).
Its name intentionally omits ComputerCraft, Minecraft, Cobalt and CCLuau.
Package/API name: LuauRuntime; public native entrypoint family: Lr*; ABI v1.
The repository is a *generic* embedded-Luau runtime distribution, not a
repackaging of any CC: Tweaked implementation.

- **Primary candidate:** official https://github.com/luau-lang/luau, MIT,
  linked at a **single full Git commit SHA** for both compiler and VM. For
  reproducible research, upstream master was observed at
  8387cfb461b38ce09e37c1e4c2811538ef1bf5cb on 2026-10-15;
  this is a **candidate observation**, not an approved production pin or proof
  that the candidate builds. M3 must freeze, hash and qualify its selected SHA.
  Avoid moving branches, mutable tags, unverified release binaries, mismatched
  compiler/VM revisions and downloading source at build time without lock/hash.
- **Build:** standalone CMake C17/C++17 adapter and Luau.Compiler/Luau.VM,
  without CLI, analysis, native code generation/JIT or exposed bytecode loading.
  Minimize transitive dependencies. Produce separately named Windows x64 and
  Linux x64 artifacts, a local ABI conformance harness and deterministic build
  manifests (source SHA, toolchain, build flags, CRT/stdlib, dependency license,
  ABI major/minor, hashes and exported symbols). Packaging can use static
  upstream Luau libraries inside one private runtime helper; the public ABI is
  the independently defined C entry table below, not raw lua_State or C++ ABI.
- **License:** MIT is the proposed license for wholly original generic wrapper
  files; preserve Roblox/Lua MIT notices, other third-party notices and an
  auditable source/SBOM inventory. Independently authored wrapper code and
  tests must contain no copied CCPL code, ILuaMachine/ILuaContext declarations,
  CC: Tweaked ROM, assets, generated signatures, nor Minecraft classes.
- **Boundary:** the generic repository owns VM creation, compile, ABI validation,
  marshalling, sandbox, request suspension, resource counters and standalone
  adversarial tests. CCLuau owns Java bridge/transport, ComputerId and boot
  fencing, host capability policy, launcher, terminal, event routing, main-thread
  world commands and device APIs. The generic runtime must also work with a
  synthetic standalone host unrelated to Minecraft.
- **Containment choice:** for M4, prefer a **supervised helper process** that
  links the generic library, instead of loading untrusted native code directly
  into the game JVM. IPC may carry the same framed ABI-level messages but is a
  separate, versioned transport; it does not expose OS pointers. Crash, hang
  and compilation DoS isolation are not supplied by a mere DLL/JNI boundary.
  M3 must evaluate packaging, process startup/recovery, OS memory controls,
  failure injection and transport integrity. If this is infeasible, an in-process
  alternative requires a new written risk decision and cannot claim fatal fault
  containment.

Official evidence: [Luau README](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/README.md),
[build options](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/CMakeLists.txt),
[license](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/LICENSE.txt)
and [security policy](https://github.com/luau-lang/luau/security/policy).
Luau explicitly does *not* guarantee termination/resource exhaustion safety.
No backend replacement is selected without a reproducible M3 failure report.

## D2 — Native ABI v1 (normative proposed contract, not source code)

The ABI is independently specified and is implementation neutral. Stable public
entrypoint: **LrQueryApi(requestedMajor, minimumMinor, callerTableBytes,
outApiTable)**, plus one size/version-checked function table. ABI major **1**,
initial minor **0**. Unknown major => ABI_UNSUPPORTED; a larger required minor
=> ABI_UNSUPPORTED; newer tables preserve earlier prefixes. Each struct begins
with uint32 StructBytes, uint16 Major and uint16 Minor. Check all sizes, alignment,
integer overflow, reserved zero fields and input pointers *before* invoking a
backend. Caller and callee must agree on 64-bit little-endian x64; no silently
portable-by-accident binary assumptions.

### ABI surface and legal transitions

| V1 function | Input / required output | Constraints |
| --- | --- | --- |
| LrCreateRuntime | versioned limits/config -> RuntimeHandle, BackendManifest | creates an owning runtime instance; no script or CC object |
| LrCloseRuntime | RuntimeHandle -> OK / ALREADY_CLOSED / BUSY | idempotent after all sessions close; BUSY never frees live VM |
| LrCreateSession | runtime, limits, capability set -> SessionHandle | fresh isolated Luau state and allocator per session |
| LrCloseSession | SessionHandle -> OK / ALREADY_CLOSED / BUSY | only on owner executor; cleanup once; BUSY while step executing |
| LrCompileSource | session, UTF-8 source bytes, length, chunk name -> CompiledHandle or diagnostic | input is trusted length-delimited source; no user bytecode import |
| LrDropCompiled | CompiledHandle -> OK / ALREADY_CLOSED | handle tied to exactly one session; no use after close |
| LrStart | session, compiled handle, copied value-vector -> StepStatus | executes first entry under protected VM resume |
| LrResume | yielded session, copied value-vector -> StepStatus | only for an eligible user yield; not for WAIT_HOST/WAIT_EVENT |
| LrCompleteHost | WAIT_HOST session, request ID, success/error and copied values -> StepStatus | exact outstanding request; old/duplicate/out-of-order responses rejected |
| LrDeliverEvent | WAIT_EVENT session, name and copied values -> StepStatus | host must prefilter against saved event filter; one event at a time |
| LrReadMessage | session, caller-owned output buffer/capacity -> type/bytes-required | drains output/request/diagnostic messages after a step; no internal pointer escape |
| LrGetMetrics | session -> versioned snapshot | heap used/peak, pending counts, interrupt/slice info, final error |
| LrCancel | session, reason -> CANCEL_REQUESTED/ALREADY_TERMINAL/INVALID_HANDLE | only operation callable off the owner thread; signals atomics, never touches lua_State |

These are *logical* signatures; M3 will author a compilable C header with explicit
stdint types, field offsets, export calling conventions and ABI-layout tests.
Opaque handles are 64-bit checked IDs containing runtime-instance identity and
per-slot generation; **never** exported pointers, JNI references, file
descriptors, C++ types or VM stack indices. No handle reuse while an instance is
alive. Lookup/close/cancel races must use a safe registry acquisition mechanism;
the Cancel path cannot dereference freed memory. A closing instance makes every
subsequent operation fail closed. Cross-instance, cross-session and closed-handle
operations return typed errors; none dereference stale native pointers.

All functions other than LrCancel require the *single recorded owner thread* of
the session; wrong-thread calls return WRONG_THREAD without touching VM state.
A runtime instance may own multiple sessions, but every v1 session owns a
separate Luau VM/heap and one host-scheduled foreground coroutine. Other Luau
coroutines are not independent host schedulers. Host calls from unsupported
non-yieldable frames/coroutines produce YIELD_NOT_ALLOWED, not a blocked JNI
callback. M3 must verify this distinction for metamethods, protected calls and
native callbacks.

### Ownership, buffers and errors

- Caller owns source, input frame and destination output buffers; contents are
  copied/validated before a step uses them. Output is copied into caller-allocated
  memory; BUFFER_TOO_SMALL returns the *required* size and leaves the message
  queued. No cross-CRT free, callback-owned pointer or borrowed VM string.
- Compiled source is VM-instance local; bytecode is never accepted from the
  caller, written to persistent storage, or reused between backend revisions.
  Compilation and VM loading occur within the controlled native component.
  Host cannot supply a private Luau bytecode blob via the public ABI.
- Native entrypoints and C++ callbacks contain exceptions/longjmp wholly inside
  their native protected boundary; no C++ exception unwinds through C, IPC or
  JNI. Use upstream protected resume APIs, not unprotected lua_call. A native
  crash, abort, OOM killer or deadlock cannot be recovered with Java catch.
- Each result has StatusCode, FailureClass, a bounded UTF-8 message and optional
  trace data. Suggested classes: SYNTAX, SCRIPT_ERROR, HOST_ERROR, DENIED,
  SERIALIZATION_ERROR, RESOURCE_LIMIT, TIMEOUT, CANCELLED, WRONG_THREAD,
  INVALID_HANDLE, ABI_UNSUPPORTED, NATIVE_FAILURE and BACKEND_UNAVAILABLE.
  A status identifies whether a session is still valid. Traces are truncated,
  sanitized, non-modal and prefixed in CCLuau logs with [Runtime:Luau].
- All input/output fields are length-delimited. No NUL termination contract;
  log text and chunk names are normalized to valid UTF-8. Error messages never
  include unchecked filesystem paths, native addresses or unlimited payloads.
- No foreign callback invoked synchronously from native into Java during a
  Luau resume. Java/IPC dispatch runs only *after* native returns a host request.
  Generic native C functions are short-lived and only prepare a request/yield.

## D3 — Framed host protocol and copied values

ABI messages and optional helper-process IPC have independent version fields.
IPC outer frame: LengthLE32, ProtocolMajorLE16, ProtocolMinorLE16,
ProcessInstanceId128, SessionHandle64, Sequence64, MessageKindLE16,
PayloadLengthLE32, PayloadBytes. Enforce size and consistency before decoding;
a process restart invalidates the instance ID. Transport delivery may be
at-most-once; it must not silently replay world mutations after reconnection.
Use one monotonic sequence per session, no wraparound. The Java owner maintains
the authoritative (ComputerId, BootGeneration, SessionId) fence *outside*
the generic runtime. Never pass that Minecraft-specific tuple into the generic
repository as a public requirement.

**V1 value envelope**, little endian and length-prefixed, uses tags NIL,
FALSE, TRUE, FINITE_F64 (IEEE-754, normalize negative zero), UTF8_STRING,
BYTE_STRING, ARRAY, MAP and OPAQUE_CAPABILITY. Arrays carry explicit count and
preserve nil slots/argument arity. Map keys are unique UTF-8 strings **including the empty string**, or
exact signed 32-bit integers; reject unsupported keys and duplicate canonical
keys. Capability tokens are opaque uint64 IDs, scoped to a session, type,
permitted operations and revocation generation. The host resolves them; no raw
Java/OS/VM pointer values. Maps encode keys in deterministic order and all lengths
are checked with overflow-safe arithmetic. All strings for service names and
event names are valid UTF-8; separate BYTE_STRING carries arbitrary bytes.

Lua tables are copied recursively under a bounded work budget; cycles are
**rejected** with CYCLIC_VALUE, repeated acyclic subgraphs are copied with no
identity preservation, and metamethods/functions/userdata/threads are rejected
unless mapped to a deliberately minted opaque capability. Traversal uses raw
table operations; no user metamethod invocation during serialization. Limit
nesting, nodes and total encoded bytes *before* Java or native commits a request.
A hostile value must fail predictably without exceeding recursion/native stack.
No cross-VM closure, Lua registry handle, table reference, metatable or module
cache is transported.

**Exact v1 encoding rule:** after each containing frame's checked length, each
value is [Tag:U8][Body], where 0x00=NIL (zero bytes), 0x01=FALSE (zero),
0x02=TRUE (zero), 0x03=FINITE_F64 (eight little-endian bytes),
0x04=UTF8_STRING and 0x05=BYTE_STRING (U32LE byte count then bytes),
0x06=ARRAY (U32LE element count followed by that many encoded values),
0x07=MAP (U32LE pair count, each followed by key/value), and
0x08=OPAQUE_CAPABILITY (U64LE token plus U32LE capability type and
U32LE revocation epoch). MAP keys are encoded with 0x04 or reserved 0x09
SIGNED_I32_KEY (I32LE body), never with general floating-point tags.
0x09 is invalid outside map-key position. Unknown tags, extra trailing bytes,
non-canonical map order, non-finite numbers, ambiguous negative zero,
oversized lengths, invalid UTF-8 and forged capability epochs are rejected.
Do not decode untrusted bytes via a native recursive call stack; use a
bounded explicit traversal stack. The encoding deliberately excludes graphs
and integer values outside keys; application numbers use finite F64.


**Host request**: Session + RequestId + OperationId + CapabilityId + typed
value-vector + deadline. At most **one outstanding host request in v1**; the
session transitions to WAIT_HOST and returns immediately to the supervisor.
Host dispatch checks capability scope, ownership, policy, budget and current
generation before enqueuing any work. Non-world terminal operations may execute
through the Cobalt computer host executor; world work must be admitted/executed
on the authorized server thread. Completion is a copied success/error vector
with *the same* request ID, delivered only on the VM owner thread. A duplicate,
wrong-generation, late, aborted or mismatched completion is counted/discarded and
must never restart a closed session. No implicit retries of side effects.
Request cancellation before dispatch is a no-op; once an authorized world
operation has begun, cancellation cannot undo its side effect. The result may
be discarded without claiming the world mutation was rolled back.

**Event wait**: an independently authored, generic AwaitEvent native primitive
installed by the embeddable runtime yields a requested filter and produces
WAIT_EVENT; the CCLuau adapter may expose that primitive through a later typed
Luau API without copying stock Cobalt implementation. WAIT_EVENT records an
exact filter or wildcard; Luau event
delivery is explicitly selected by the CCLuau host, not directly wired to the
shared Cobalt event queue. The actual stock asynchronous task event is
**task_complete**, singular: LuaContext and TaskCallback use this string even
though ILuaContext's inherited Javadoc says task_completed. CCLuau must translate
stock task IDs/results into *fenced* host completions; it must not expose native
request IDs as authoritative CC task IDs or trust only a script-visible event.
No event may advance more than one session continuation. Termination is an
out-of-band cancel signal and must not wait behind a full normal-event queue.
Critical host completions require a reliable bounded mailbox/acknowledgment or
terminal failure on overflow, not an assumed delivery guarantee from the stock
256-entry ComputerExecutor event queue.

## D4 — Session state and terminal lifecycle

~~~text
CREATED --CompileSource(success)--> READY --Start--> RUNNING
       --compile rejection--> CREATED (retry or close)
RUNNING --host request--> WAIT_HOST --matching response--> RUNNING
RUNNING --event wait--> WAIT_EVENT --selected event--> RUNNING
RUNNING --explicit yield--> YIELDED --Resume--> RUNNING
RUNNING --return--> COMPLETED
RUNNING --error/limit/deadline--> FAILED / TIMED_OUT / RESOURCE_EXHAUSTED
ANY NONTERMINAL --Cancel--> CANCEL_REQUESTED --ack/forced exit--> CANCELLED
ANY NONRUNNING --CloseSession--> CLOSED
~~~

CANCEL_REQUESTED is a revocation overlay, not permission to resume. A VM that
cannot reach a safe interruption point stays in cancellation pending until the
external supervisor terminates its isolated helper process. Never release VM
storage while its owner thread executes. Late success after cancellation does
not transition a cancelled session back to RUNNING. A process death fails every
session assigned to that helper; no transparent replay of host requests.
COMPLETE/FAILED/etc. is reported once to the launcher, then handles are closed
and terminal rights are returned.

**CCLuau adapter (future M4; not implemented):**
1. Cobalt remains the one BIOS/shell machine. An explicit ROM-side Luau runner
   starts a managed child using a host API; first-line language dispatch is M5,
   and ordinary shell.execute's direct load path must not be assumed handled.
   No directive remains Lua. A Luau failure never falls back to Cobalt.
2. The Cobalt runner yields/awaits one internal completion ticket while the
   child executes; Cobalt is not replaced or closed. Preserve arguments,
   working-directory semantics, errors and existing shell/os.run contracts.
   Nested managed Luau foreground sessions, multishell, redirected monitors,
   HTTP direct loaders and cross-VM require remain unsupported until separately
   qualified. No concurrent Cobalt/Luau terminal writers in v1.
3. On start, acquire an exclusive **per-computer foreground terminal lease** with
   (ComputerId, BootGeneration, SessionId, LeaseEpoch). Only that lease may apply
   child terminal operations. Cobalt launcher does not write while child owns it;
   complete/revoke the lease on success, error, terminate, shutdown, reboot and
   unload. Stale writes are dropped before touching terminal state.
4. Cobalt still receives and handles host events; the adapter routes child-
   eligible events into its private bounded mailbox while the launcher waits.
   Preserve Cobalt event filters/terminate behavior; do not consume/drop unrelated
   shell events without an explicit documented policy. Completion wakes only its
   owning launcher ticket after identity validation; avoid spoofable os.queueEvent
   names as the sole completion authority.
5. Invalidate/revoke the boot/session lease **before** initiating close, then
   cancel pending requests, reject queued callbacks and drain/drop copied
   responses. Increment BootGeneration before any new VM admission; SessionId
   never reused within a boot. A full ComputerId reuse after world migration
   still needs a fresh host instance epoch/boot generation.
6. Existing LuaContext.issueMainThreadTask queues ordinary Runnables; it does
   *not* itself prevent a task from executing after shutdown. GuardedLuaContext
   illustrates validity checks but is not proof of a complete generation fence.
   Thus M4 must fence **at admission, again at main-thread execution immediately
   before side effects, and again on completion**, plus invalidate on every
   terminal transition. An already-entered nontransactional world operation is
   allowed to finish but is not retried or reported as cancelled-before-commit.
   Queue removal alone is insufficient. No raw JNI or Java references in Luau.

Source anchors:
[ComputerExecutor](../../projects/core/src/main/java/dan200/computercraft/core/computer/ComputerExecutor.java),
[LuaContext](../../projects/core/src/main/java/dan200/computercraft/core/computer/LuaContext.java),
[TaskCallback](../../projects/core-api/src/main/java/dan200/computercraft/api/lua/TaskCallback.java),
[GuardedLuaContext](../../projects/core/src/main/java/dan200/computercraft/core/computer/GuardedLuaContext.java),
[TimeoutState](../../projects/core/src/main/java/dan200/computercraft/core/computer/TimeoutState.java),
[ProgramEntry](ProgramEntry.md), and the executed M1 [qualification ledger](../Qualification.md).

## D5 — Sandbox, watchdog and resource profile

Official Luau exposes lua_newstate(custom allocator), protected lua_resume,
lua_yield, lua_pushcclosurek (yield continuation), lua_isyieldable,
luaL_sandbox, luaL_sandboxthread, and a per-VM interrupt callback invoked at
loop/call/return/GC safepoints. **Luau does not promise a hard CPU/instruction
limit, nor a compiler resource-exhaustion bound.** Interrupt callbacks cannot
simply force coroutine yield from arbitrary native/GC frames; C API yield is
disallowed across certain C-call/metamethod boundaries. Debug single-step exists
but must be measured for instruction accounting and overhead. A long blocking
C callback or compiler pass may not reach a VM interrupt. Callback debug-name
pointers supplied to lua_pushcclosurek must outlive the VM. Do not catch a
native crash with Java exceptions or assume luaL_sandbox grants access-policy
checks for host-provided functions.

Proposed **M3 trial quotas** below are defaults to test, **not proven caps**.
The helper/supervisor may tighten them; changes require versioned configuration,
metrics and a qualification result. Existing stock Cobalt timeout (7 s soft,
1.5 s abort period) is unchanged and does not constitute Luau watchdog proof.

| Resource | Proposed v1 admission budget | Enforcement / open question |
| --- | --- | --- |
| UTF-8 source/chunk name | 256 KiB / 256 bytes | reject before compiler; verify UTF-8 and overflow |
| Compiled representation | 2 MiB per session | wrapper rejects oversized compile output; compiler intermediate memory not covered |
| Luau heap | 16 MiB live allocations per session | lua_newstate allocator hard reject with overflow checks; verify OOM unwind |
| Serialized value | 256 KiB/frame; 64 KiB/string; depth 16; 4,096 visited nodes | bounded iterative decoder/encoder, preflight sizes |
| Event mailbox | 64 messages / session, 256 KiB aggregate | bounded admission; backpressure/overflow semantics |
| Host requests | 1 outstanding/session; 64 admitted per second | exact request IDs, bucketed dispatch budget, no synchronous JNI callback |
| Diagnostics/output | 64 KiB/session queued, 8 KiB/error | truncation with counted drops; never block VM on log sink |
| Compiler wall time | 2 s supervisor watchdog trial | **only helper-process termination is hard**; source limit alone not enough |
| Uninterrupted VM step | 250 ms soft-interrupt trial; 1.5 s hard helper kill grace | safepoint response latency/GC callback safety must be measured |
| Instruction limit | desired 1 million/step | **EXPERIMENTAL**: debugstep/accounting or validated instrumented mode, no hard instruction claim |
| Native/helper RSS | 128 MiB initial process budget | OS Job Object/cgroup/RLIMIT or equivalent; verify enforcement per platform |
| Host callback/blocking time | 10 ms per admitted synthetic request target | main-thread admission budget/async; cannot preempt running world operation |
| Sessions | 1 active foreground child/computer | per-computer lease and global service cap to be specified in M4 |

At VM init, expose only approved standard functions and host capabilities; no
raw OS filesystem/process/network, foreign library, debug privilege, Java
reflection, raw Lua bytecode, native module loader, arbitrary environment entry
or unsafe userdata pointer. Apply luaL_sandbox and thread-specific globals; all
custom tables/objects must enforce readonly and receiver/capability checks as
appropriate. Disable Luau native code generation/JIT initially. A sandbox error
must fail the child only; process-level escape or native fatality is a blocked
M4 condition pending containment evidence.

Evidence:
[official C API](https://luau.org/api/),
[sandboxing guide](https://luau.org/sandbox/),
[VM lua.h at research SHA](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/VM/include/lua.h),
[VM luaconf.h](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/VM/include/luaconf.h),
[compiler C API](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/Compiler/include/luacode.h),
[yield/resume implementation](https://github.com/luau-lang/luau/blob/8387cfb461b38ce09e37c1e4c2811538ef1bf5cb/VM/src/ldo.cpp),
and [upstream compiler DoS discussion](https://github.com/luau-lang/luau/discussions/1274).
Upstream describes nontermination/resource exhaustion as outside its guarantees.
C/C++ exceptions versus longjmp and callback safety are build-specific M3
verification tasks, not presumed guarantees.

## D6 — M3 standalone executable qualification matrix

M3 uses a **synthetic independent host** (no Cobalt, Java, Minecraft, CCPL
code). Run on native **Windows x64 and Linux x64** with the exact locked upstream
and wrapper source SHAs. Each case reports raw commands, versions, case counts,
timeouts, per-case memory/CPU peaks, exit code, output hashes and artifact hashes.
Pass at one OS does not imply pass at the other. Fatal/error-injection cases are
isolated in disposable child processes.

| M3 case | Required executable assertion (both platforms) |
| --- | --- |
| Build and ABI layout | clean pinned-source builds; expected symbols; ABI version/size negotiation and wrong major/minor |
| Compile/run/error | source -> valid program, strict syntax failure, runtime error, exact arg/result nil arity, no external bytecode |
| Sandbox | forbidden host APIs absent; readonly globals, distinct session heaps/globals, no unsafe pointers |
| Yield/continuation | start, explicit yield, resumed values, host request suspends and synthetic response resumes exactly once |
| Non-yieldable contexts | metamethod/C/protected call cases return typed failure without unwinding across ABI |
| Event handling | filtered/wildcard events, queued event limits, terminate/cancel precedence and no completion spoof |
| Infinite loops | tight numeric loop, empty while, nested calls and recursion reach typed timeout or isolated kill under bounds |
| Instruction semantics | instruction counter trial versus safepoint behavior at optimization levels; **no PASS if exact bound is unproven** |
| Heap/OOM | allocator cap reached, allocation denial and recovery/closure; no allocator double free or zombie handle |
| Compiler DoS | pathological nesting/large-but-admitted source; measure watchdog and helper kill, no parent hang |
| Value marshalling | invalid UTF-8, overflow, duplicate/invalid map keys, NaN/Inf, cycles, alias sharing, depth/node/byte limits |
| Host request races | delayed, duplicate, wrong request, cancelled-before-admit, cancel-after-dispatch, stale-after-restart |
| Cancellation race | cancel while WAIT_HOST, event wait, active resume, compiler and callback; never invoke freed session |
| Threading | wrong-thread calls rejected; concurrent Cancel versus Close; use-after-close and close while RUNNING -> BUSY |
| Terminal outputs | synthetic lease and ownership revocation, no stale writes; not a Minecraft terminal test |
| Lifecycle | **1,000 create/compile/run/yield/close cycles per platform** minimum, plus repeated failures/restarts; no outstanding handles |
| Native allocation | allocator reaches zero live bytes after close; tracked heap/RSS growth bounded and documented |
| Fatal containment | crash/abort/deadlock injected into isolated helper; supervisor reports failure, kills helper and continues |
| Packaging | reproducible manifests/hashes, loader library discovery, no extraneous native dependencies, license inventory |

**M3 exit is not granted** by passing only VM self-tests. Hard stop/hang/crash
behaviors and cleanup across process boundaries must be demonstrated in the
standalone host. If a hard quota is unavailable, the ledger must say PARTIAL,
and a feature requiring that guarantee remains blocked. Preserve the roadmap
minimum of 1,000 lifecycles; do not reduce it for expedience. M4 additionally
needs both-loader Java integration and the pending M1 stale-main-thread
callback and terminal ownership tests.

## D7 — Known blockers and decision status

| Gate | Status on M2 | Required resolution |
| --- | --- | --- |
| Official Luau suitability | STATIC CANDIDATE | pin candidate, build/probe on both OSes; compare C continuations and allocator under stress |
| ABI v1 policy | DESIGNED, NOT IMPLEMENTED | M3 compile C header/layout tests and real checked handles |
| VM instruction/time limits | EXPERIMENTAL | prove safepoint/watchdog behavior; no yield promise from interrupt |
| Compiler memory/CPU | UNBOUNDED IN-PROCESS | helper-process quotas/death/restart; alternative needs new risk decision |
| Callback lifetimes | UNQUALIFIED | native debug names, thread callbacks and error unwinding tests |
| Main-thread stale results | M1 OPEN | pre-side-effect generation fence and post-result rejection under reboot/unload races in M4 |
| Terminal/multishell | M1 OPEN | single foreground lease first; broad redirection/multishell deferred |
| Fatal helper containment | DESIGN ONLY | kill/abort/hang injection must not take down parent |
| License compliance | NOT CLEARED | CCPL §5 dependency comparability, MPL/CCPL file-level inventory, MIT Luau notices and distribution counsel |
| Release | NOT AUTHORIZED | M9 artifact review, source/SBOM and legal clearance |

**M2 verdict: PARTIAL.** Repository ownership, provisional name, primary
backend, ABI v1 and M3 experiments are specified by static evidence. Feasibility,
resource and safety guarantees, cross-platform results and distribution legality
remain unproven. M3 may begin *standalone only* under an explicit work order;
M4/Minecraft/native release is not authorized.

For licensing rationale see [LicenseInventory.md](../LicenseInventory.md).
Repository separation supports provenance; it is not a CCPL §5 exemption.
