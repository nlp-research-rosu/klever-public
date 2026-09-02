#!/usr/bin/env python3
"""Print one satisfiable entry-claim substitution and both Python results."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable


def load_entry(path: Path, name: str) -> Callable[[list[str], str], list[str]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


def int_seq(text: str) -> str:
    result = ".IntSeq"
    for codepoint in reversed([ord(character) for character in text]):
        result = f"iCons({codepoint}, {result})"
    return result


def str_seq(strings: list[str]) -> str:
    result = ".StrSeq"
    for string in reversed(strings):
        result = f"ssCons({int_seq(string)}, {result})"
    return result


def val_seq(strings: list[str]) -> str:
    result = ".ValSeq"
    for string in reversed(strings):
        result = f"vCons(str({int_seq(string)}), {result})"
    return result


def main() -> int:
    strings = ["abc", "bacd", "cde", "array"]
    substring = "a"
    canonical = load_entry(Path("/reference/canonical.py"), "ground_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/run/solution.py"), "ground_generated"
    )
    canonical_result = canonical(strings.copy(), substring)
    generated_result = generated(strings.copy(), substring)
    record = {
        "input": {"strings": strings, "substring": substring},
        "entry_substitution": {
            "SS": str_seq(strings),
            "P": int_seq(substring),
        },
        "claimed_filterStrings_normal_form": val_seq(canonical_result),
        "trusted_canonical_result": canonical_result,
        "generated_solution_result": generated_result,
    }
    print(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True))
    if canonical_result != generated_result:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
