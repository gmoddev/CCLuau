# SPDX-FileCopyrightText: 2026 gmoddev
#
# SPDX-License-Identifier: MPL-2.0

"""Inventory production Java LuaFunction declarations, not dynamic runtime exports."""

import argparse
import csv
import io
import re
from pathlib import Path


def GetInventory(Root):
    Rows = []
    AnnotationPattern = re.compile(r"^[ \t]*@LuaFunction(?P<Options>\([^)]*\))?", re.MULTILINE)
    DeclarationPattern = re.compile(r"\bpublic\s+([^;{]*?)\s*(?:\{|;)", re.DOTALL)
    MethodPattern = re.compile(r"(\w+)\s*\((.*?)\)\s*(?:throws\s+.*)?$", re.DOTALL)
    for Source in sorted((Root / "projects").glob("*/src/main/java/**/*.java")):
        Content = Source.read_text(encoding="utf-8")
        ModuleMatch = re.search(r"@cc\.module\s+(\S+)", Content)
        LicenseMatch = re.search(r"SPDX-License-Identifier:\s*([^\r\n]+)", Content)
        for Annotation in AnnotationPattern.finditer(Content):
            # Scan only up to the next annotation; fail rather than silently omit a declaration.
            End = Content.find("@LuaFunction", Annotation.end())
            Tail = Content[Annotation.end():End if End != -1 else len(Content)]
            Declaration = DeclarationPattern.search(Tail)
            Method = MethodPattern.search(Declaration.group(1).strip()) if Declaration else None
            if not Method:
                raise ValueError(f"Unrecognized declaration in {Source.relative_to(Root)}")
            Options = Annotation.group("Options") or ""
            Names = re.findall(r'"([^"\n]+)"', Options) or [Method.group(1)]
            for Name in Names:
                Rows.append({
                    "Source": Source.relative_to(Root).as_posix(),
                    "SourceLicense": LicenseMatch.group(1).strip() if LicenseMatch else "UNRESOLVED",
                    "Line": Content.count("\n", 0, Annotation.start()) + 1,
                    "Class": Source.stem,
                    "ModuleHint": ModuleMatch.group(1) if ModuleMatch else "",
                    "Method": Method.group(1),
                    "LuaName": Name,
                    "JavaSignature": " ".join(Declaration.group(1).split()),
                    "MainThread": str(bool(re.search(r"mainThread\s*=\s*true", Options))).lower(),
                    "Unsafe": str(bool(re.search(r"unsafe\s*=\s*true", Options))).lower(),
                })
    if not Rows:
        raise ValueError("No LuaFunction declarations found")
    Buffer = io.StringIO(newline="")
    Writer = csv.DictWriter(Buffer, fieldnames=list(Rows[0]), lineterminator="\n")
    Writer.writeheader()
    Writer.writerows(Rows)
    return Buffer.getvalue(), len(Rows)


def Main():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument("--check", action="store_true", help="Check the checked-in census without writing")
    Options = Parser.parse_args()
    Root = Path(__file__).resolve().parents[1]
    Output = Root / "docs" / "NativeApiInventory.csv"
    Content, Count = GetInventory(Root)
    if Options.check:
        if not Output.exists() or Output.read_text(encoding="utf-8") != Content:
            raise SystemExit("[Baseline:ApiInventory] Census is missing or outdated")
        print(f"[Baseline:ApiInventory] Verified {Count} declaration/alias rows")
    else:
        Output.write_text(Content, encoding="utf-8", newline="")
        print(f"[Baseline:ApiInventory] Wrote {Count} declaration/alias rows to {Output}")


if __name__ == "__main__":
    Main()
