#!/usr/bin/env python3
"""Ground witnesses for every entry precondition and its claimed result."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def balanced_tail(codes: str, depth: int) -> bool:
    for character in codes:
        if character == " ":
            continue
        if character == "(":
            depth += 1
        elif character == ")" and depth > 0:
            depth -= 1
        else:
            return False
    return depth == 0


def scan_groups(codes: str, current: str, depth: int, accumulated: list[str]) -> list[str]:
    result = list(accumulated)
    for character in codes:
        if character == " ":
            continue
        current += character
        if character == "(":
            depth += 1
        else:
            depth -= 1
        if depth == 0:
            result.append(current)
            current = ""
    return result


def main() -> int:
    trusted = load(Path("/reference/canonical.py"), "claim_trusted")
    generated = load(Path("/candidate/solution.py"), "claim_generated")

    # A complete loop-head state satisfying the all-balanced-inputs claim:
    # env=1; H=7; ACC=["seed"]; CUR="("; DEPTH=1; CODES=") ()";
    # OLD="", INPUT="(placeholder)", RESTSCOPES contains the normal module and
    # builtins scopes.  The heap contains only 7 |-> list(ACC).
    loop = {
        "claim": "all-balanced-inputs",
        "codes": ") ()",
        "current": "(",
        "depth": 1,
        "accumulated": ["seed"],
    }
    loop["balancedTail"] = balanced_tail(loop["codes"], loop["depth"])
    loop["parenSpaceOnly"] = all(c in " ()" for c in loop["codes"])
    loop["depthNonnegative"] = loop["depth"] >= 0
    loop["currentCondition"] = loop["depth"] > 0 or loop["current"] == ""
    loop["claimed_heap_list"] = scan_groups(
        loop["codes"], loop["current"], loop["depth"], loop["accumulated"]
    )
    print(json.dumps(loop, sort_keys=True))

    entries = {
        "all-balanced-calls": "() (()) (()())",
        "empty": "",
        "prompt-example": "( ) (( )) (( )( ))",
        "adjacent-and-spaced": "  (()())() ",
        "deep-nesting": "(((())))",
    }
    mismatch_count = 0
    for claim, value in entries.items():
        result = {
            "claim": claim,
            "input": value,
            "balancedTail": balanced_tail(value, 0),
            "parenSpaceOnly": all(c in " ()" for c in value),
            "claimed_scanGroups": scan_groups(value, "", 0, []),
            "trusted_python": trusted.separate_paren_groups(value),
            "generated_python": generated.separate_paren_groups(value),
        }
        if not (
            result["claimed_scanGroups"]
            == result["trusted_python"]
            == result["generated_python"]
        ):
            mismatch_count += 1
        print(json.dumps(result, sort_keys=True))
    print(f"mismatch_count={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
