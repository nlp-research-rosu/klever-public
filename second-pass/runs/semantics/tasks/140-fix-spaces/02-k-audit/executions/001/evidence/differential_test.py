#!/usr/bin/env python3
"""Independent candidate/canonical/prompt-contract differential for HumanEval 140."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/140-fix-spaces/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/differential-inputs.jsonl")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fix_spaces


def prompt_model(text: str) -> str:
    """Direct model of the prose: runs of 1/2 spaces become '_'/'__'; >2 becomes '-'."""
    output: list[str] = []
    index = 0
    while index < len(text):
        if text[index] != " ":
            output.append(text[index])
            index += 1
            continue
        end = index
        while end < len(text) and text[end] == " ":
            end += 1
        run_length = end - index
        output.append("-" if run_length > 2 else "_" * run_length)
        index = end
    return "".join(output)


def build_cases() -> list[tuple[str, str]]:
    documented = [
        ("example-no-space", "Example"),
        ("example-one-internal", "Example 1"),
        ("example-one-leading", " Example 2"),
        ("example-three-internal", " Example   3"),
    ]
    explicit_boundaries = [
        ("empty", ""),
        ("only-1-space", " "),
        ("only-2-spaces", "  "),
        ("only-3-spaces", "   "),
        ("only-4-spaces", "    "),
        ("trailing-1", "a "),
        ("trailing-2", "a  "),
        ("trailing-3", "a   "),
        ("leading-1", " a"),
        ("leading-2", "  a"),
        ("leading-3", "   a"),
        ("internal-0", "ab"),
        ("internal-1", "a b"),
        ("internal-2", "a  b"),
        ("internal-3", "a   b"),
        ("internal-4", "a    b"),
        ("two-runs", "  a   b  "),
        ("non-ascii", "é  🙂"),
        ("other-whitespace", "a\t\nb"),
        ("nul", "a\x00 b"),
    ]

    exhaustive: list[tuple[str, str]] = []
    alphabet = (" ", "a", "b")
    for length in range(0, 8):
        for chars in itertools.product(alphabet, repeat=length):
            text = "".join(chars)
            exhaustive.append((f"exhaustive-{length}", text))

    rng = random.Random(140)
    random_alphabet = (" ", "a", "Z", "_", "\t", "\n", "é", "🙂", "\x00")
    generated: list[tuple[str, str]] = []
    for number in range(1000):
        length = rng.randrange(0, 41)
        text = "".join(rng.choice(random_alphabet) for _ in range(length))
        generated.append((f"generated-{number}", text))

    # Preserve order but remove duplicate strings so each tested input is explicit.
    cases: list[tuple[str, str]] = []
    seen: set[str] = set()
    for label, text in documented + explicit_boundaries + exhaustive + generated:
        if text not in seen:
            seen.add(text)
            cases.append((label, text))
    return cases


def main() -> int:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical_140")
    candidate = load_function(CANDIDATE_PATH, "submitted_solution_140")
    cases = build_cases()

    mismatch_candidate_canonical: list[dict[str, object]] = []
    mismatch_candidate_prompt: list[dict[str, object]] = []
    mismatch_canonical_prompt: list[dict[str, object]] = []

    with INPUTS_PATH.open("w", encoding="utf-8") as inputs_file:
        for index, (label, text) in enumerate(cases):
            inputs_file.write(
                json.dumps({"index": index, "label": label, "text": text}, ensure_ascii=True)
                + "\n"
            )
            canonical_result = canonical(text)
            candidate_result = candidate(text)
            prompt_result = prompt_model(text)
            row = {
                "index": index,
                "label": label,
                "input": text,
                "canonical": canonical_result,
                "candidate": candidate_result,
                "prompt_model": prompt_result,
            }
            if candidate_result != canonical_result:
                mismatch_candidate_canonical.append(row)
            if candidate_result != prompt_result:
                mismatch_candidate_prompt.append(row)
            if canonical_result != prompt_result:
                mismatch_canonical_prompt.append(row)

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print(f"inputs_artifact={INPUTS_PATH}")
    print(f"tested_inputs={len(cases)}")
    print(f"candidate_vs_canonical_mismatches={len(mismatch_candidate_canonical)}")
    print(f"candidate_vs_prompt_model_mismatches={len(mismatch_candidate_prompt)}")
    print(f"canonical_vs_prompt_model_mismatches={len(mismatch_canonical_prompt)}")
    print("first_candidate_vs_canonical_mismatches:")
    for row in mismatch_candidate_canonical[:20]:
        print(json.dumps(row, ensure_ascii=True, sort_keys=True))

    # A nonzero result makes the material trusted-canonical divergence unmistakable.
    return 1 if mismatch_candidate_canonical else 0


if __name__ == "__main__":
    sys.exit(main())
