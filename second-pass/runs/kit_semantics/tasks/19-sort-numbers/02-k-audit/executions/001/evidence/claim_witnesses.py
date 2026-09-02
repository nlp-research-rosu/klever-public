#!/usr/bin/env python3
"""Ground witnesses for every entry claim and Python-side result comparison."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)
RESULT_PATH = Path("/audit-output/evidence/04-claim-witnesses.json")


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def split_ws_ascii(value: str) -> list[str]:
    current = ""
    result = []
    for char in value:
        if ord(char) in {32, 9, 10, 13}:
            if current:
                result.append(current)
                current = ""
        else:
            current += char
    if current:
        result.append(current)
    return result


def main() -> int:
    canonical = load_module("trusted_canonical_witness", "/reference/canonical.py")
    candidate = load_module(
        "candidate_witness", "/tmp/audit-work/19-sort-numbers/solution.py"
    )
    sample = "three one five"
    tokens = split_ws_ascii(sample)
    sort_claim = {
        "claim": "sort-numbers",
        "input": sample,
        "codepoints": [ord(char) for char in sample],
        "splitWS_tokens": tokens,
        "precondition_allNumberWords": all(token in WORDS for token in tokens),
        "canonical_result": canonical.sort_numbers(sample),
        "candidate_result": candidate.sort_numbers(sample),
        "claimed_summary_after_one_unfold": (
            'str(joinCodes(strToCodes(" "), '
            "sortKeyVS(splitWS(CS,.IntSeq,.ValSeq),numberKeyClosure)))"
        ),
    }
    key_claims = []
    for index, word in enumerate(WORDS):
        actual = candidate._number_key(word)
        key_claims.append(
            {
                "claim": f"key-{word}",
                "input": word,
                "precondition": "true (no requires clause)",
                "candidate_result": actual,
                "claimed_result": index,
                "match": actual == index,
            }
        )
    result = {
        "sort_claim": sort_claim,
        "key_claims": key_claims,
        "all_witnesses_satisfiable": sort_claim["precondition_allNumberWords"],
        "all_python_results_match": (
            sort_claim["canonical_result"] == sort_claim["candidate_result"]
            and all(item["match"] for item in key_claims)
        ),
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["all_witnesses_satisfiable"] and result["all_python_results_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
