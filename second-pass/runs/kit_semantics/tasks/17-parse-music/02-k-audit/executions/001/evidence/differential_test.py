#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for valid music strings."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from itertools import product
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/candidate-src/solution.py")
CORPUS_PATH = Path("/audit-output/evidence/differential_inputs.jsonl")
NOTES = ("o", "o|", ".|")
PROMPT_EXAMPLE = "o o| .| o| o| .| .| .| .| o o"


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_music


def add_case(cases: dict[str, set[str]], category: str, text: str) -> None:
    cases.setdefault(text, set()).add(category)


def build_cases() -> dict[str, set[str]]:
    cases: dict[str, set[str]] = {}
    add_case(cases, "documented-example", PROMPT_EXAMPLE)

    branch_cases = {
        "empty": "",
        "delimiter-current-zero": " ",
        "whole-end-flush": "o",
        "whole-pipe-current-four": "o|",
        "quarter-pipe-current-nonfour": ".|",
        "delimiter-flush-current-four": "o o",
        "delimiter-no-flush-current-zero": "o| ",
        "leading-trailing-empty-fields": "  o|  .|  ",
    }
    for name, text in branch_cases.items():
        add_case(cases, f"branch:{name}", text)

    # Exhaust all note sequences through length six, with every supported
    # separator width and leading/trailing empty-field layout.
    for length in range(7):
        for notes in product(NOTES, repeat=length):
            if not notes:
                for text in ("", " ", "   "):
                    add_case(cases, "exhaustive-length-0", text)
                continue
            for width in (1, 2, 3):
                separator = " " * width
                body = separator.join(notes)
                for text in (
                    body,
                    separator + body,
                    body + separator,
                    separator + body + separator,
                ):
                    add_case(cases, f"exhaustive-length-{length}", text)

    # Deterministic broader samples over the same unrestricted valid grammar.
    rng = random.Random(170017)
    for _ in range(5000):
        length = rng.randrange(0, 101)
        notes = [rng.choice(NOTES) for _ in range(length)]
        if not notes:
            text = " " * rng.randrange(0, 9)
        else:
            parts = [" " * rng.randrange(0, 9)]
            for index, note in enumerate(notes):
                if index:
                    parts.append(" " * rng.randrange(1, 9))
                parts.append(note)
            parts.append(" " * rng.randrange(0, 9))
            text = "".join(parts)
        add_case(cases, "generated-length-0..100", text)

    for note, category in (
        ("o", "boundary-4096-whole"),
        ("o|", "boundary-4096-half"),
        (".|", "boundary-4096-quarter"),
    ):
        add_case(cases, category, ("   ".join([note] * 4096)))
    mixed = [NOTES[index % len(NOTES)] for index in range(4096)]
    add_case(cases, "boundary-4096-mixed", "  ".join(mixed))
    return cases


def outcome(function, text: str):
    try:
        return ("return", function(text))
    except Exception as error:  # Evidence preserves any unexpected divergence.
        return ("raise", type(error).__name__, str(error))


def main() -> None:
    canonical = load_entry("trusted_canonical_parse_music", CANONICAL_PATH)
    generated = load_entry("candidate_generated_parse_music", GENERATED_PATH)
    cases = build_cases()

    corpus_digest = hashlib.sha256()
    mismatches = []
    category_counts: dict[str, int] = {}
    with CORPUS_PATH.open("w", encoding="utf-8") as corpus:
        for index, (text, categories) in enumerate(cases.items()):
            record = {
                "index": index,
                "categories": sorted(categories),
                "input": text,
            }
            line = json.dumps(record, ensure_ascii=True, separators=(",", ":"))
            corpus.write(line + "\n")
            corpus_digest.update((line + "\n").encode())
            for category in categories:
                category_counts[category] = category_counts.get(category, 0) + 1
            expected = outcome(canonical, text)
            actual = outcome(generated, text)
            if expected != actual:
                mismatches.append(
                    {
                        "index": index,
                        "input": text,
                        "canonical": expected,
                        "generated": actual,
                    }
                )

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print(f"corpus={CORPUS_PATH}")
    print(f"cases={len(cases)}")
    print(f"corpus_sha256={corpus_digest.hexdigest()}")
    print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:5], ensure_ascii=True))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
