<!-- SPDX-FileCopyrightText: 2026 gmoddev
SPDX-License-Identifier: MPL-2.0 -->

# Proposed Luau facade and raw query APIs

Design only; none of this surface exists in the current runtime. Existing Lua APIs
remain unchanged. New objects are capability-bound, receiver-checked, versioned
and generation-fenced; ordinary computers cannot acquire turtle movement methods.

```lua
--lang luau
--!strict

local Result = self:Move(Enum.MoveDirection.Forward, 5)
local Villagers = computer:GetService("Villagers")
local Villager = Villagers:InspectAdjacent(Enum.Direction.Front)

if Villager then
    local Trades = Villager:GetTrades()
    for Index, Offer in Trades do
        print(Index, Offer.Result.ItemId, Offer.Uses, Offer.MaxUses)
    end

    local Matches = Villager:FindTrades({
        ItemId = "minecraft:enchanted_book",
        EnchantmentId = "minecraft:mending",
        MinLevel = 1,
    })
end
```

`computer` is the service root; `self` is the current device. They may refer to the
same computer identity but expose different typed capabilities. GetService is
explicitly provisioned; an unsupported service reports a local capability error.
InspectAdjacent returns nil when no eligible target exists, with an optional
second reason value for inaccessible/unavailable targets. World reads occur on
the server thread. Reach, occlusion, supported sides, upgrade requirements, and
multi-entity selection remain design gates rather than guessed game behavior.

## Raw data first

`Villager:GetTrades()` returns `{ [number]: TradeOfferSnapshot }`, a copied read-only
dictionary keyed by **1-based offer Index** in the observed Minecraft offer order.
It contains all observed offers, including exhausted offers. Empty existing offers
return an empty dictionary. Ungenerated/unreadable offers must be distinguishable
at inspection time from a genuinely generated empty set. Index is snapshot-local,
not a durable trade ID. Dictionary iteration order is unspecified; sort numeric
keys when ordering matters. Never key by item ID: multiple offers can share an item.

`Villager:GetInfo()` returns snapshot metadata: Id (ephemeral opaque token),
Profession, Level, IsAdult, OffersGenerated, ObservedTick and SnapshotVersion.
The object is an immutable observation, not a live entity reference. GetTrades
and FindTrades perform no further world reads. Reinspect to obtain fresh data.

| TradeOfferSnapshot field | Proposed meaning |
| --- | --- |
| Index | 1-based offer key, valid within this snapshot only |
| InputA / InputB | Base item requirements; second may be absent |
| Result | ItemStackSnapshot with ItemId, Count and bounded component-derived detail |
| Uses / MaxUses / Available | Current exhaustion observation; no reservation |
| Xp / PriceMultiplier / Demand / SpecialPriceDiff | Observed merchant metadata when reliably available |
| EffectiveCost / PriceContext | Optional contextual price; never invent a player discount |

ItemStackSnapshot has PascalCase fields ItemId, Count, Enchantments and
StoredEnchantments, with enchantment entries keyed by registry ID and numeric
level. Read MC 26.3 components, not translated names or guessed NBT strings.
Exact exposed component detail needs a bounded schema and loader qualification.

FindTrades takes ItemId (matches Result.ItemId), EnchantmentId (matches stored
enchantments for books, ordinary enchantments for other items), MinLevel (default
1 when EnchantmentId is present), and AvailableOnly (default false). Reject unknown
fields, non-positive/non-integer levels and MinLevel without EnchantmentId.
Return the same indexed dictionary shape and preserve original offer indexes.
Apply all predicates to the existing snapshot. Changing helper filters cannot
reveal anything absent from GetTrades. No Match means an empty dictionary.

## Device primitives before convenience

Expose GetFuel, Inspect, Detect, GetInventory, Move and Turn over existing host
authority. Move accepts Forward/Back/Up/Down and an integer count 1..64 (default
Forward, 1); returns Success, Completed, Requested and optional Reason. Execute
one existing command per step and stop at first failure. Partial movement has no
rollback. No hidden digging, refuelling, chunk loading, pathfinding or retries.
Facade failure reasons should map documented stock errors without changing Lua
results. Pathfinding and actual villager trade execution are separate future RFCs.

Write type declarations and runtime-shape checks after implementing the surface,
not fake stubs claiming working APIs during the baseline phase.
