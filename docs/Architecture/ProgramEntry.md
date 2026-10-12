<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Program-entry inventory

Static source trace at the baseline. All paths currently execute Lua/Cobalt;
`--lang luau` is currently an ordinary comment and provides no runtime selection.
Paths below are relative to projects/core/src/main/resources/data/computercraft/lua/.

| Entry | Existing route | Future scope / required evidence |
| --- | --- | --- |
| Power-on | ComputerExecutor.createLuaMachine -> bios.lua -> os.run shell/multishell | Always Cobalt BIOS; no factory replacement |
| shell.run | rom/programs/shell.lua: tokenise -> shell.execute -> executeProgram -> load(source, env) -> protected execution | Explicit runner first; qualify direct shell dispatch separately |
| shell.execute | Same executeProgram path, but preserves argument boundaries instead of tokenising concatenated command line | Preserve arg[0], args, working directory, environment and result |
| Shebang | executeProgram checks first line #!, resolves interpreter, recursively dispatches (budget 100) | Preserve stock behavior; first-line language comment and shebang cannot both be authoritative |
| Root/disk startup, startup directory, autorun | rom/startup.lua resolves files -> shell.run | Inherits shell dispatch; qualify file order/settings/disk precedence |
| os.run | bios.lua -> loadfile(path, env) -> pcall(chunk) | Independent route; launcher must yield and return the existing success contract |
| multishell.launch / shell.openTab | rom/programs/advanced/multishell.lua -> coroutine -> os.run; window redirection/event filters | Initial Luau sessions unsupported here until terminal/event ownership qualified |
| parallel.waitForAny / waitForAll | rom/apis/parallel.lua resumes Lua functions with event filters | Not a program loader; no raw Luau closures in a Lua coroutine set |
| loadfile / dofile | bios.lua reads source -> load; dofile invokes the returned closure | Remain same-runtime chunk APIs; cannot return a native Luau closure |
| load / loadstring | Cobalt chunk compilation, directly used by shell and HTTP runners | Remain Lua; cannot transparently switch heap/runtime |
| require | shell creates package via rom/modules/main/cc/require.lua; file loader uses loadfile and a package cache | Separate Luau module loader/cache; reject cross-language imports |
| os.loadAPI | bios.lua -> loadfile in API environment | Legacy Lua only; no VM substitution |
| wget run / pastebin run | rom/programs/http/*.lua -> load(fetched source, text mode, environment) | Explicit future source runner needed; shell patch alone does not cover this |
| REPL / custom loaders / addons | Arbitrary Lua load/coroutine/API usage | Inventory external callers; no automatic Luau promise |

The shell's comment says "using os.run", but its implementation compiles directly.
The implementation is the evidence. Do not design dispatch solely from that comment.

## Proposed header rules

Accept exactly `--lang lua` or `--lang luau` on the first logical line after an
optional UTF-8 BOM, with outer whitespace and LF/CRLF. No header means Lua,
including files named .luau. Unknown language directives get a terminal diagnostic
before running. `--!strict` may follow on line two. Do not rewrite source.

An explicit future `luau <file>` runner selects Luau when the header is absent;
reject a contradictory `--lang lua` header. Program boundaries select runtimes;
module imports and chunks do not switch the running VM. Native unavailability
fails that program, returning control to the Lua shell without reinterpretation.

Tests must cover starts, return values, syntax errors, user errors, terminate,
nested shell calls, redirected terminals, reboot, poweroff, argument packing,
event filters and queued host results. Broader automatic header routing comes
only after the explicit runner passes those gates.
