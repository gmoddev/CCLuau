# SPDX-FileCopyrightText: 2026 gmoddev
#
# SPDX-License-Identifier: MPL-2.0

"""Audit JUnit reports; the CC GameTest reporter encodes optional failures as skipped."""

import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as Xml


def GetSummary(File, GameTest=False):
    Cases = list(Xml.parse(File).getroot().iter("testcase"))
    Result = {
        "Report": str(File), "Sha256": hashlib.sha256(File.read_bytes()).hexdigest(),
        "Total": len(Cases), "Passed": 0, "Failed": [], "OptionalFailures": [], "Skipped": [],
    }
    for Case in Cases:
        Failure = Case.find("failure")
        if Failure is None:
            Failure = Case.find("error")
        Skipped = Case.find("skipped")
        if Failure is not None:
            Result["Failed"].append({"Name": Case.get("name"), "Message": Failure.get("message")})
        elif Skipped is not None:
            Result["OptionalFailures" if GameTest else "Skipped"].append({
                "Name": Case.get("name"), "Message": Skipped.get("message"),
            })
        else:
            Result["Passed"] += 1
    Result["Status"] = "BLOCKED" if not Cases else (
        "PARTIAL" if Result["Failed"] or Result["OptionalFailures"] or Result["Skipped"] else "PASS"
    )
    return Result


def Main():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument("reports", type=Path, nargs="+")
    Parser.add_argument("--gametest", action="store_true", help="Interpret skipped as executed optional failures")
    Parser.add_argument("--output", type=Path)
    Options = Parser.parse_args()
    Results = [GetSummary(File, Options.gametest) for File in Options.reports]
    Content = json.dumps(Results, indent=2) + "\n"
    if Options.output:
        Options.output.write_text(Content, encoding="utf-8")
    print(Content, end="")
    raise SystemExit(any(Result["Status"] != "PASS" for Result in Results))


if __name__ == "__main__":
    Main()
