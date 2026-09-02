#!/usr/bin/env python3
"""Independent three-way differential test for HumanEval 140."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import re
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/candidate-src/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/02-differential-inputs.jsonl")


def import_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fix_spaces


def contract_oracle(text: str) -> str:
    """Directly encode the prose: 3+ spaces -> '-', otherwise each -> '_'."""
    return re.sub(r" {3,}", "-", text).replace(" ", "_")


def add(cases: list[tuple[str, str]], seen: set[str], label: str, text: str) -> None:
    if text not in seen:
        seen.add(text)
        cases.append((label, text))


def build_cases() -> list[tuple[str, str]]:
    cases: list[tuple[str, str]] = []
    seen: set[str] = set()

    documented = [
        "Example",
        "Example 1",
        " Example 2",
        " Example   3",
    ]
    for index, text in enumerate(documented):
        add(cases, seen, f"documented-{index}", text)

    explicit = [
        "",
        " ",
        "  ",
        "   ",
        "    ",
        "     ",
        "a",
        "a ",
        "a  ",
        "a   ",
        "a    ",
        " a",
        "  a",
        "   a",
        "    a",
        "a b",
        "a  b",
        "a   b",
        "a    b",
        " a  b   c    ",
        "\t \n",
        "\u00a0  \u2603",
        "\U0001f642   \U0001f680  ",
    ]
    for index, text in enumerate(explicit):
        add(cases, seen, f"boundary-{index}", text)

    for run_length in range(0, 7):
        run = " " * run_length
        for shape_name, text in [
            ("only", run),
            ("prefix", run + "x"),
            ("suffix", "x" + run),
            ("interior", "x" + run + "y"),
            ("two-runs", run + "x" + run),
        ]:
            add(cases, seen, f"branch-run-{run_length}-{shape_name}", text)

    exhaustive_alphabet = (" ", "a", "\t", "\u00e9")
    for length in range(0, 7):
        for chars in itertools.product(exhaustive_alphabet, repeat=length):
            add(cases, seen, f"exhaustive-length-{length}", "".join(chars))

    rng = random.Random(140_20260729)
    random_alphabet = (
        " ",
        "a",
        "B",
        "_",
        "-",
        "\t",
        "\n",
        "\u00a0",
        "\u00e9",
        "\u2603",
        "\U0001f642",
        "\U0001f680",
        "\x00",
    )
    for index in range(5000):
        length = rng.randrange(0, 81)
        text = "".join(rng.choice(random_alphabet) for _ in range(length))
        add(cases, seen, f"random-{index}", text)

    return cases


def main() -> int:
    canonical = import_entry(CANONICAL_PATH, "trusted_canonical_140")
    generated = import_entry(GENERATED_PATH, "generated_solution_140")
    cases = build_cases()

    corpus_digest = hashlib.sha256()
    candidate_canonical_mismatches: list[dict[str, object]] = []
    candidate_contract_mismatches: list[dict[str, object]] = []
    canonical_contract_mismatches: list[dict[str, object]] = []
    with INPUTS_PATH.open("w", encoding="utf-8") as output:
        for index, (label, text) in enumerate(cases):
            encoded = json.dumps(
                {"index": index, "label": label, "text": text},
                ensure_ascii=True,
                sort_keys=True,
            )
            output.write(encoded + "\n")
            corpus_digest.update((encoded + "\n").encode())

            canonical_result = canonical(text)
            generated_result = generated(text)
            contract_result = contract_oracle(text)
            record = {
                "index": index,
                "label": label,
                "input": text,
                "canonical": canonical_result,
                "generated": generated_result,
                "contract": contract_result,
            }
            if generated_result != canonical_result:
                candidate_canonical_mismatches.append(record)
            if generated_result != contract_result:
                candidate_contract_mismatches.append(record)
            if canonical_result != contract_result:
                canonical_contract_mismatches.append(record)

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print("contract_oracle=re.sub(r' {3,}', '-', text).replace(' ', '_')")
    print(
        "scope=4 documented examples; explicit empty/Unicode/control and "
        "run-length 0..6 boundaries in five positions; exhaustive lengths "
        "0..6 over {space,a,tab,e-acute}; 5000 deterministic random strings "
        "of lengths 0..80 over 13 code points"
    )
    print(f"cases={len(cases)}")
    print(f"inputs_sha256={corpus_digest.hexdigest()}")
    print(
        "generated_vs_canonical_mismatches="
        f"{len(candidate_canonical_mismatches)}"
    )
    print(
        "generated_vs_contract_mismatches="
        f"{len(candidate_contract_mismatches)}"
    )
    print(
        "canonical_vs_contract_mismatches="
        f"{len(canonical_contract_mismatches)}"
    )
    print("first generated-vs-canonical mismatches:")
    for record in candidate_canonical_mismatches[:30]:
        print(json.dumps(record, ensure_ascii=True, sort_keys=True))
    if candidate_contract_mismatches:
        print("first generated-vs-contract mismatches:")
        for record in candidate_contract_mismatches[:30]:
            print(json.dumps(record, ensure_ascii=True, sort_keys=True))

    # This command is specifically a generated-vs-trusted-canonical differential.
    return 1 if candidate_canonical_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
