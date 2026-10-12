<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Source ownership map

Root-relative landmarks verified against the pinned source. See upstream
[projects/ARCHITECTURE.md](../../projects/ARCHITECTURE.md) for the original overview;
its Forge terminology predates the NeoForge dependency in this branch.

| Layer | Source | Owns / future integration boundary |
| --- | --- | --- |
| Public host contracts | projects/core-api/src/main/java/dan200/computercraft/api/lua/ | ILuaAPI, ILuaContext, LuaFunction, MethodResult, argument/value contracts |
| Host construction | projects/core/src/main/java/dan200/computercraft/core/ComputerContext.java | Scheduler and machine factories; Cobalt default |
| Boot/lifecycle | projects/core/src/main/java/dan200/computercraft/core/computer/ComputerExecutor.java | One machine, API registration, BIOS, events, power commands, shutdown |
| Runtime | projects/core/src/main/java/dan200/computercraft/core/lua/ | ILuaMachine, MachineEnvironment, CobaltLuaMachine, argument conversion |
| Scheduler | projects/core/src/main/java/dan200/computercraft/core/computer/computerthread/ | Worker scheduling and timeouts; retain host supervision |
| Main-thread execution | projects/core/src/main/java/dan200/computercraft/core/computer/mainthread/ | Server-thread task budgets and callbacks |
| Native Lua APIs | projects/core/src/main/java/dan200/computercraft/core/apis/ | Files, terminals, OS, peripherals, redstone, HTTP and handles |
| Method binding | projects/core/src/main/java/dan200/computercraft/core/methods/ and core/asm/ | Annotated Java methods, generated adapters and results |
| ROM | projects/core/src/main/resources/data/computercraft/lua/ | bios.lua, ROM APIs, modules, startup, shell and utilities |
| Minecraft host | projects/common/src/main/java/dan200/computercraft/shared/computer/core/ | ServerComputer, ComputerSystem and game lifecycle |
| Turtle surface | projects/common/src/main/java/dan200/computercraft/shared/turtle/apis/TurtleAPI.java | Script methods delegate to authoritative commands |
| Turtle implementation | projects/common/src/main/java/dan200/computercraft/shared/turtle/core/ | TurtleBrain, command queue, fuel, move/turn/dig/place/inspect |
| Peripherals | projects/common/src/main/java/dan200/computercraft/shared/peripheral/ | Disk drives, monitors, modems, printers, speakers, generic inventory/fluid/energy |
| Other devices | projects/common/src/main/java/dan200/computercraft/shared/pocket/ and shared/computer/apis/ | Pocket upgrades and command computer APIs |
| Loader adaptation | projects/fabric/, projects/forge/, projects/common/.../shared/platform/ | PlatformHelper implementations, registration, loader hooks; forge is NeoForge |
| Client boundary | projects/common/src/client/ | Screens/rendering/input; no server runtime dependency on client classes |
| Standalone | projects/standalone/ | No-Minecraft host useful for later runtime qualification |
| Tests | projects/core/src/test/, projects/common/src/testMod/ | Java/ROM unit tests and Kotlin GameTests |
| Build | settings.gradle.kts, build-logic/base/src/main/kotlin/, gradle/ | Multi-project toolchains, packaging, lint and publishing tasks |

Place future VM-neutral session supervision in core without Minecraft dependencies.
Keep CC-specific JNI adapters in this fork and generic native VM code outside it.
Villager access belongs in common with loader policy hooks where required. Do not
couple the separate VM repository to these implementation classes.
