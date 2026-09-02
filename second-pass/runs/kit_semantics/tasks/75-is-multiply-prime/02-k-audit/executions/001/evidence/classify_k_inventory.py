#!/usr/bin/env python3
"""Assign an audit disposition to every item emitted by k_inventory.py."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from k_inventory import items  # noqa: E402


ON_PATH: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13, 14, 25, 36, 37, 38, 39, 40, 41, 42, 49,
        124, 125, 126, 127, 130, 131, 132, 157, 158,
        185, 186, 189, 190, 191, 194, 199, 200, 210, 213, 214, 215,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "semantics/call.k": {19, 20, 21, 69},
    "semantics/operators.k": {15, 16, 17},
    "semantics/bool.k": {16, 17, 18, 20, 22, 24},
    "semantics/int.k": {26},
}


def relative_key(path: Path) -> str:
    parts = path.as_posix().split("/")
    if "semantics" in parts:
        index = parts.index("semantics")
        return "/".join(parts[index:index + 2])
    return path.name


def disposition(path: Path, line: int, kind: str, attrs: list[str]) -> str:
    key = relative_key(path)
    if path.name == "spec.k" and kind == "claim":
        return "TARGET_CLAIM_RESULT_CONSTRAINING"
    if "no-evaluators" in attrs or "symbol" in attrs:
        return "OPAQUE_UNUSED_NO_DEPENDENCY"
    if path.name == "concrete.k" or "concrete" in attrs:
        return "CONCRETE_ONLY_NOT_IN_PROOF"
    if line in ON_PATH.get(key, set()):
        return "ON_PATH_SOUND"
    if path.name == "verification.k":
        return "PROOF_LOCAL_EXTENSION"
    return "OFF_PATH_REVIEWED_NO_TASK_WITNESS"


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: classify_k_inventory.py FILE...")
    print("file\tline\tkind\tattributes\tdisposition\tsource")
    for raw in sys.argv[1:]:
        path = Path(raw)
        for line, kind, attrs, text in items(path):
            fields = [
                str(path), str(line), kind, ",".join(attrs),
                disposition(path, line, kind, attrs),
                text.replace("\t", " "),
            ]
            print("\t".join(fields))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
