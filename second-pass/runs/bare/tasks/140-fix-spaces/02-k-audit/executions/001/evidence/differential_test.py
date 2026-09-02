#!/usr/bin/env python3
"""Independent differential test for HumanEval 140 (fix_spaces)."""

from __future__ import annotations

import importlib.util
import hashlib
import itertools
import json
from pathlib import Path


def load_entry(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fix_spaces


def prompt_literal_oracle(text: str) -> str:
    """Direct run-based reading of the prompt, independent of both programs."""
    out: list[str] = []
    i = 0
    while i < len(text):
        if text[i] != " ":
            out.append(text[i])
            i += 1
            continue
        j = i
        while j < len(text) and text[j] == " ":
            j += 1
        width = j - i
        out.append("-" if width > 2 else "_" * width)
        i = j
    return "".join(out)


canonical = load_entry("trusted_canonical", "/reference/canonical.py")
submitted = load_entry("submitted_solution", "/tmp/audit-work/src/solution.py")

documented = {
    "Example": "Example",
    "Example 1": "Example_1",
    " Example 2": "_Example_2",
    " Example   3": "_Example-3",
}

boundaries = [
    "",
    " ",
    "  ",
    "   ",
    "    ",
    "a",
    " a",
    "  a",
    "   a",
    "    a",
    "a ",
    "a  ",
    "a   ",
    "a    ",
    "a b",
    "a  b",
    "a   b",
    "a    b",
    " a ",
    "  a  ",
    "   a   ",
    "a b  ",
    "a  b ",
    "a   b  ",
    "a    b   ",
    "a _- b",
    "é  λ",
    "\t  \n",
    "a" * 500,
    "a" * 900,
    "a" * 1100,
    " " * 500,
    " " * 900,
    " " * 1100,
]

generated = [
    "".join(chars)
    for length in range(0, 9)
    for chars in itertools.product((" ", "a", "b"), repeat=length)
]

ordered_inputs = list(dict.fromkeys([*documented, *boundaries, *generated]))
Path("/audit-output/evidence/differential_inputs.jsonl").write_text(
    "".join(json.dumps({"input": text}, ensure_ascii=False) + "\n" for text in ordered_inputs),
    encoding="utf-8",
)
mismatches_canonical: list[dict[str, object]] = []
mismatches_prompt: list[dict[str, object]] = []
documented_failures: list[dict[str, object]] = []


def outcome(function, text: str) -> dict[str, str]:
    try:
        return {"kind": "value", "value": function(text)}
    except Exception as error:  # The exception itself is part of program behavior.
        return {"kind": "exception", "type": type(error).__name__}


def summarize_text(text: str) -> str | dict[str, object]:
    if len(text) <= 80:
        return text
    return {
        "length": len(text),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "prefix": text[:20],
        "suffix": text[-20:],
    }


def summarize_outcome(result: dict[str, str]) -> dict[str, object]:
    if result["kind"] == "exception":
        return result
    return {"kind": "value", "value": summarize_text(result["value"])}


for text in ordered_inputs:
    got = outcome(submitted, text)
    expected_canonical = outcome(canonical, text)
    expected_prompt = outcome(prompt_literal_oracle, text)
    if got != expected_canonical:
        mismatches_canonical.append(
            {
                "input": summarize_text(text),
                "submitted": summarize_outcome(got),
                "canonical": summarize_outcome(expected_canonical),
            }
        )
    if got != expected_prompt:
        mismatches_prompt.append(
            {
                "input": summarize_text(text),
                "submitted": summarize_outcome(got),
                "prompt_oracle": summarize_outcome(expected_prompt),
            }
        )
    documented_expected = {"kind": "value", "value": documented[text]} if text in documented else None
    if text in documented and got != documented_expected:
        documented_failures.append(
            {
                "input": text,
                "submitted": summarize_outcome(got),
                "documented_expected": documented[text],
            }
        )

summary = {
    "documented_examples": len(documented),
    "explicit_boundary_cases": len(boundaries),
    "generated_scope": {
        "alphabet": [" ", "a", "b"],
        "lengths": [0, 8],
        "count_including_duplicates_with_explicit_cases": len(generated),
    },
    "unique_inputs_checked": len(ordered_inputs),
    "documented_failures": documented_failures,
    "canonical_mismatch_count": len(mismatches_canonical),
    "canonical_first_20_mismatches": mismatches_canonical[:20],
    "prompt_oracle_mismatch_count": len(mismatches_prompt),
    "prompt_oracle_first_20_mismatches": mismatches_prompt[:20],
}
print(json.dumps(summary, ensure_ascii=False, indent=2))

raise SystemExit(
    1
    if documented_failures or mismatches_canonical or mismatches_prompt
    else 0
)
