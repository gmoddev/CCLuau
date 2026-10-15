// SPDX-FileCopyrightText: 2022 The CC: Tweaked Developers
//
// SPDX-License-Identifier: MPL-2.0

package dan200.computercraft.gametest

import dan200.computercraft.gametest.api.GameTest
import dan200.computercraft.gametest.api.Timeouts
import dan200.computercraft.gametest.api.sequence
import dan200.computercraft.gametest.api.thenComputerOk
import net.minecraft.gametest.framework.GameTestHelper

class CraftOs_Test {
    /** Capture exports from real Cobalt boots on normal/advanced computers and a turtle. */
    @GameTest(timeoutTicks = Timeouts.COMPUTER_TIMEOUT)
    fun Baseline_runtime_inventory(Helper: GameTestHelper) = Helper.sequence {
        thenComputerOk("normal")
        thenComputerOk("advanced")
        thenComputerOk("turtle")
    }

    /**
     * Sends a rednet message to another a computer and back again.
     */
    @GameTest(timeoutTicks = Timeouts.COMPUTER_TIMEOUT)
    fun Sends_basic_rednet_messages(context: GameTestHelper) = context.sequence { thenComputerOk("main") }
}
