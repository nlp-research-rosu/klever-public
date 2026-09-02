#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 101."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


FIXED_PATH = Path("/audit-output/evidence/differential/fixed-inputs.json")
CANONICAL_PATH = Path("/tmp/audit-work/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/candidate/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_string


def prompt_oracle(text: str) -> list[str]:
    """Literal comma/U+0020 splitting stated by the prompt."""
    return [word for word in text.replace(",", " ").split(" ") if word]


def main() -> None:
    canonical = load_entry(CANONICAL_PATH, "trusted_humaneval_101")
    candidate = load_entry(CANDIDATE_PATH, "candidate_humaneval_101")
    fixed = json.loads(FIXED_PATH.read_text())

    exhaustive = [
        "".join(chars)
        for length in range(9)
        for chars in itertools.product(("a", "B", ",", " "), repeat=length)
    ]

    random_generator = random.Random(101_20260726)
    random_cases: list[str] = []
    alphabet = tuple("abcXYZ019") + (",", " ", "é", "λ", "東")
    for _ in range(10_000):
        length = random_generator.randrange(0, 81)
        random_cases.append(
            "".join(random_generator.choice(alphabet) for _ in range(length))
        )

    intended_cases = fixed + exhaustive + random_cases
    extended_python_whitespace = [
        "\t",
        "\n",
        "\r",
        "\v",
        "\f",
        "\u00a0",
        "alpha\tbeta",
        " alpha\nbeta, gamma ",
        "\u2003alpha,\u2009beta",
    ]

    mismatches: list[dict[str, object]] = []
    for text in intended_cases:
        expected = canonical(text)
        actual = candidate(text)
        contract = prompt_oracle(text)
        if actual != expected or actual != contract:
            mismatches.append(
                {
                    "input": text,
                    "canonical": expected,
                    "candidate": actual,
                    "prompt_oracle": contract,
                }
            )

    extended_mismatches = []
    for text in extended_python_whitespace:
        expected = canonical(text)
        actual = candidate(text)
        if actual != expected:
            extended_mismatches.append(
                {"input": text, "canonical": expected, "candidate": actual}
            )

    corpus_digest = hashlib.sha256(
        json.dumps(
            intended_cases,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    print(f"fixed_cases={len(fixed)}")
    print(
        "exhaustive_cases="
        f"{len(exhaustive)} alphabet=['a','B',',',' '] lengths=0..8"
    )
    print(
        "generated_cases="
        f"{len(random_cases)} seed=10120260726 lengths=0..80"
    )
    print(f"intended_corpus_sha256={corpus_digest}")
    print(f"intended_mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:10], ensure_ascii=False, indent=2))
    print(f"extended_python_whitespace_cases={len(extended_python_whitespace)}")
    print(f"extended_candidate_canonical_mismatches={len(extended_mismatches)}")
    if extended_mismatches:
        print(json.dumps(extended_mismatches, ensure_ascii=False, indent=2))

    assert not mismatches
    assert not extended_mismatches
    print("DIFFERENTIAL_TEST=PASS")


if __name__ == "__main__":
    main()
