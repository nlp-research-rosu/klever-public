#!/usr/bin/env python3
"""Ground substitutions for the end-to-end K claim's result term."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fix_spaces


def pending_spaces(count: int) -> list[int]:
    if count > 2:
        return [45]
    if count == 1:
        return [95]
    if count == 2:
        return [95, 95]
    return []


def fix_spaces_loop(accumulator: list[int], remaining: list[int], count: int) -> list[int]:
    accumulator = list(accumulator)
    for code in remaining:
        if code == 32:
            count += 1
        else:
            accumulator.extend(pending_spaces(count))
            accumulator.append(code)
            count = 0
    return accumulator


def trailing_spaces(remaining: list[int], count: int) -> int:
    for code in remaining:
        count = count + 1 if code == 32 else 0
    return count


def claimed_result(text: str) -> str:
    codes = [ord(character) for character in text]
    loop_result = fix_spaces_loop([], codes, 0)
    result_codes = loop_result + pending_spaces(trailing_spaces(codes, 0))
    return "".join(chr(code) for code in result_codes)


def main() -> int:
    candidate = load(
        "/tmp/audit-work/140-fix-spaces/solution.py", "entry_witness_candidate"
    )
    canonical = load("/reference/canonical.py", "entry_witness_canonical")
    cases = [
        "",
        "Example",
        "Example 1",
        " Example   3",
        " ",
        "  ",
        "   ",
        "a  ",
        "a   b",
        "  a   b  ",
        "é  🙂",
    ]
    candidate_mismatches = 0
    canonical_mismatches = 0
    print(
        "satisfying_ground_entry_state="
        + json.dumps(
            {
                "k": "#loadAll(solutionModule) ~> Call(Name(\"fix_spaces\"), str(.IntSeq))",
                "env": 0,
                "scopes": {
                    "0": "scope(.Map,parent(-1))",
                    "-1": "builtinsScope",
                },
                "scopeLoc": 1,
                "heap": ".Map",
                "heapLoc": 0,
                "stack": ".List",
                "ret": "noRet",
                "exc": "NoExc",
                "exit-code": 0,
            },
            sort_keys=True,
        )
    )
    for text in cases:
        claimed = claimed_result(text)
        candidate_result = candidate(text)
        canonical_result = canonical(text)
        row = {
            "input": text,
            "claimed_result": claimed,
            "candidate": candidate_result,
            "canonical": canonical_result,
            "candidate_matches_claim": candidate_result == claimed,
            "canonical_matches_claim": canonical_result == claimed,
        }
        print(json.dumps(row, ensure_ascii=True, sort_keys=True))
        candidate_mismatches += candidate_result != claimed
        canonical_mismatches += canonical_result != claimed
    print(f"candidate_vs_claim_mismatches={candidate_mismatches}")
    print(f"canonical_vs_claim_mismatches={canonical_mismatches}")
    return 1 if candidate_mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
