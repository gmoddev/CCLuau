# SPDX-FileCopyrightText: 2026 gmoddev
#
# SPDX-License-Identifier: MPL-2.0

"""Test the census validator's failure handling with synthetic data, not a VM."""

import csv
import unittest
from pathlib import Path

from ValidateRuntimeInventory import Validate


class RuntimeInventoryTest(unittest.TestCase):
    def runTest(self):
        Root = Path(__file__).resolve().parents[1]
        with (Root / "docs/NativeApiInventory.csv").open(encoding="utf-8", newline="") as Stream:
            Rows = list(csv.DictReader(Stream))
        Owners = {
            "OSAPI": "os", "FSAPI": "fs", "TermAPI": "term", "TermMethods": "term",
            "RedstoneAPI": "redstone", "RedstoneMethods": "redstone",
            "PeripheralAPI": "peripheral", "HTTPAPI": "http",
        }
        Apis = {Name: [] for Name in Owners.values()}
        for Row in Rows:
            if Row["Class"] in Owners:
                Apis[Owners[Row["Class"]]].append(Row["LuaName"])
        with self.subTest("complete synthetic export set"):
            self.assertEqual("PASS", Validate({"Apis": Apis}, Rows)["Status"])
        with self.subTest("missing exported method cannot pass"):
            Incomplete = {Name: list(Names) for Name, Names in Apis.items()}
            Incomplete["os"].remove("queueEvent")
            self.assertIn("queueEvent", Validate({"Apis": Incomplete}, Rows)["Missing"]["os"])
        with self.subTest("missing configured API cannot pass"):
            Incomplete = dict(Apis)
            del Incomplete["http"]
            self.assertEqual("PARTIAL", Validate({"Apis": Incomplete}, Rows)["Status"])
        with self.subTest("empty census cannot produce a vacuous pass"):
            with self.assertRaises(ValueError):
                Validate({"Apis": Apis}, [])


if __name__ == "__main__":
    unittest.main()
