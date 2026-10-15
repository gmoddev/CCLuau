# SPDX-FileCopyrightText: 2026 gmoddev
#
# SPDX-License-Identifier: MPL-2.0

"""Compare a booted core runtime's observed methods with the existing native census."""

import argparse
import csv
import json
from pathlib import Path


def Validate(Inventory, Rows):
    # Only built-in core API classes are eligible here. Device/loader/peripheral
    # exports require loader evidence; the declaration census is not that evidence.
    Owners = {
        "OSAPI": "os", "FSAPI": "fs", "TermAPI": "term", "TermMethods": "term",
        "RedstoneAPI": "redstone", "RedstoneMethods": "redstone",
        "PeripheralAPI": "peripheral", "HTTPAPI": "http",
    }
    Expected = {Name: set() for Name in Owners.values()}
    for Row in Rows:
        if Row["Class"] in Owners:
            Expected[Owners[Row["Class"]]].add(Row["LuaName"])
    Missing = {}
    Matched = 0
    for Name, Methods in sorted(Expected.items()):
        if not Methods:
            raise ValueError(f"No native declarations found for {Name}")
        Actual = set(Inventory["Apis"].get(Name, []))
        Absent = sorted(Methods - Actual)
        if Absent:
            Missing[Name] = Absent
        Matched += len(Methods & Actual)
    return {
        "Status": "PASS" if not Missing else "PARTIAL",
        "Scope": "Core API names only; signatures, behaviors, loader/device APIs and handles excluded",
        "Matched": Matched,
        "Missing": Missing,
        "ObservedCounts": {Name: len(Methods) for Name, Methods in sorted(Inventory["Apis"].items())},
    }


def Main():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument("inventory", type=Path, help="CoreRuntimeInventory.json emitted by BaselineTest")
    Parser.add_argument("--output", type=Path, help="Optional JSON result path")
    Options = Parser.parse_args()
    Root = Path(__file__).resolve().parents[1]
    Inventory = json.loads(Options.inventory.read_text(encoding="utf-8-sig"))
    with (Root / "docs/NativeApiInventory.csv").open(encoding="utf-8", newline="") as Stream:
        Result = Validate(Inventory, list(csv.DictReader(Stream)))
    Content = json.dumps(Result, indent=2, sort_keys=True) + "\n"
    if Options.output:
        Options.output.write_text(Content, encoding="utf-8")
    print(Content, end="")
    raise SystemExit(bool(Result["Missing"]))


if __name__ == "__main__":
    Main()
