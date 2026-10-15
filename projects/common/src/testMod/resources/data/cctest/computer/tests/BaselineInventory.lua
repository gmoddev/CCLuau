-- SPDX-FileCopyrightText: 2026 gmoddev
--
-- SPDX-License-Identifier: MPL-2.0

local Device = ...
local function GetNames(Value)
    local Names = {}
    for Name, Entry in pairs(Value) do
        if type(Entry) == "function" then Names[#Names + 1] = Name end
    end
    table.sort(Names)
    return Names
end

test.eq(0, os.getComputerID(), "The isolated fixture uses the imported test filesystem")
test.eq(Device == "Turtle", type(turtle) == "table", "Device capabilities must match hardware")
test.assert(type(shell.execute) == "function" and type(os.run) == "function")
test.assert(self == nil and Enum == nil and computer == nil)
local Inventory = {
    Device = Device,
    Label = os.getComputerLabel(),
    ComputerId = os.getComputerID(),
    Host = _HOST,
    IsColour = term.isColor(),
    GlobalFunctions = GetNames(_G),
    Apis = {},
}
for _, Name in ipairs({ "os", "fs", "term", "redstone", "peripheral", "http", "turtle",
    "shell", "parallel", "textutils", "settings" }) do
    if type(_ENV[Name]) == "table" then Inventory.Apis[Name] = GetNames(_ENV[Name]) end
end
fs.makeDir("M1")
local File = assert(fs.open("M1/" .. Inventory.Label .. ".json", "w"))
File.write(textutils.serializeJSON(Inventory))
File.close()
test.log("[Baseline:Inventory] Captured " .. Device)
