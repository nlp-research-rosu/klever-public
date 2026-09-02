#!/usr/bin/env python3
"""Mechanically compare the submitted program and the emitted SPEC claim."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

work = Path("/tmp/audit-work/reconstruction")


def parse(path: Path) -> dict[str, object]:
    command = [
        "kast",
        path.name,
        "--definition",
        "verification-haskell-audit",
        "--sort",
        "Pgm",
        "--output",
        "json",
    ]
    print("COMMAND:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=work,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"EXIT_STATUS: {completed.returncode}")
    if completed.returncode != 0:
        print(completed.stdout)
        raise SystemExit(f"kast failed for {path}")
    return json.loads(completed.stdout)


submitted = parse(work / "solution.mpy")

emitted_path = work / "spec-emitted-for-comparison.json"
emit_command = [
    "kprove",
    "spec.k",
    "--definition",
    "verification-haskell-audit",
    "--spec-module",
    "SPEC",
    "--dry-run",
    "--emit-json-spec",
    str(emitted_path),
    "--output",
    "none",
]
print("COMMAND:", " ".join(emit_command))
emitted = subprocess.run(
    emit_command,
    cwd=work,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)
print(f"EXIT_STATUS: {emitted.returncode}")
print(emitted.stdout.rstrip())
if emitted.returncode != 0:
    raise SystemExit("could not emit the parsed SPEC claim")

spec_json = json.loads(emitted_path.read_text())
flat_modules = spec_json["term"]["term"]
spec_module = next(module for module in flat_modules if module["name"] == "SPEC")
claim = next(
    sentence
    for sentence in spec_module["localSentences"]
    if sentence["node"] == "KClaim"
)
generated_top = claim["body"]
gcd_program_cell = next(
    arg
    for arg in generated_top["args"]
    if arg.get("label", {}).get("name") == "<gcd-program>"
)
k_cell = next(
    arg
    for arg in gcd_program_cell["args"]
    if arg.get("label", {}).get("name") == "<k>"
)
claimed = k_cell["args"][0]["lhs"]
same = submitted["term"] == claimed
print(f"submitted_sha256_source=7f5ef56c549193a381a89a8345f661aafa4e8b9d5d9f3d0bb0b522ef2b784b96")
print(f"emitted_claim_path={emitted_path}")
print(f"constructor_terms_equal={same}")
if not same:
    raise SystemExit("the entry claim does not execute the submitted constructor term")
