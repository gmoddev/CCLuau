# SPDX-FileCopyrightText: 2026 gmoddev
#
# SPDX-License-Identifier: MPL-2.0

"""Test the census validator's failure handling with synthetic data, not a VM."""

import csv
import tempfile
import unittest
from pathlib import Path

from ValidateRuntimeInventory import Validate
from SummarizeTests import GetSummary


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
        with self.subTest("a turtle profile must include the registered turtle methods"):
            Result = Validate({"Device": "Turtle", "Apis": Apis}, Rows)
            self.assertIn("forward", Result["Missing"]["turtle"])


class TestReportAudit(unittest.TestCase):
    def runTest(self):
        with tempfile.TemporaryDirectory() as Directory:
            Report = Path(Directory) / "Report.xml"
            with self.subTest("empty report cannot pass"):
                Report.write_text("<testsuite/>", encoding="utf-8")
                self.assertEqual("BLOCKED", GetSummary(Report)["Status"])
            Report.write_text('<testsuite><testcase name="A"><skipped message="optional failed"/></testcase></testsuite>', encoding="utf-8")
            with self.subTest("JUnit skipped remains unexecuted coverage"):
                Result = GetSummary(Report)
                self.assertEqual("PARTIAL", Result["Status"])
                self.assertEqual(1, len(Result["Skipped"]))
                self.assertFalse(Result["OptionalFailures"])
            with self.subTest("GameTest skipped means an optional failure, never a pass"):
                Result = GetSummary(Report, GameTest=True)
                self.assertEqual("PARTIAL", Result["Status"])
                self.assertEqual(0, Result["Passed"])
                self.assertEqual(1, len(Result["OptionalFailures"]))


if __name__ == "__main__":
    unittest.main()
