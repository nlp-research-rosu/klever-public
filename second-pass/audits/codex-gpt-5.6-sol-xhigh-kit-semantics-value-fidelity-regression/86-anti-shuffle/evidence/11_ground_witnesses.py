#!/usr/bin/env python3
"""Ground substitutions for the proof summaries and all three claim shapes."""

import importlib.util
import itertools
import json
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


def insert_code(word: tuple[int, ...], code: int) -> tuple[int, ...]:
    out: list[int] = []
    inserted = False
    for existing in word:
        if inserted:
            out.append(existing)
        else:
            if code < existing:
                out.append(code)
                inserted = True
            out.append(existing)
    if not inserted:
        out.append(code)
    return tuple(out)


def anti_shuffle_summary(codes: tuple[int, ...]) -> tuple[int, ...]:
    result: tuple[int, ...] = ()
    word: tuple[int, ...] = ()
    for code in codes:
        if code == 32:
            result = result + word + (32,)
            word = ()
        else:
            word = insert_code(word, code)
    return result + word


def k_intseq(codes: tuple[int, ...]) -> str:
    result = ".IntSeq"
    for code in reversed(codes):
        result = f"iCons({code}, {result})"
    return result


canonical = load_entry("trusted_canonical_witness", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_witness",
    Path("/tmp/audit-work/anti-shuffle-audit/solution.py"),
)

inputs = ["", "b", "ba  dc", "Hello World!!!", "dabc", " "]
for value in inputs:
    codes = tuple(map(ord, value))
    summary_codes = anti_shuffle_summary(codes)
    summary = "".join(map(chr, summary_codes))
    record = {
        "input": value,
        "input_k": k_intseq(codes),
        "summary_k": k_intseq(summary_codes),
        "summary": summary,
        "canonical": canonical(value),
        "candidate": candidate(value),
    }
    record["all_equal"] = (
        record["summary"] == record["canonical"] == record["candidate"]
    )
    print(json.dumps(record, ensure_ascii=True, sort_keys=True))
    if not record["all_equal"]:
        raise SystemExit(1)

claim_witnesses = {
    "insertion-loop": {
        "S": "b",
        "C": ord("a"),
        "B": False,
        "NW": "",
        "post_new_word": "ab",
        "post_inserted": True,
    },
    "character-loop": {
        "S": "b a",
        "A": "",
        "W": "",
        "post_result": "b ",
        "post_word": "a",
    },
    "anti-shuffle-entry": {
        "S": "ba  dc",
        "initial_env": 0,
        "initial_scope_loc": 1,
        "initial_heap": {},
        "initial_stack": [],
        "post_result": "ab  cd",
    },
}
print(json.dumps({"satisfying_claim_states": claim_witnesses}, sort_keys=True))

summary_mismatches = 0
summary_case_count = 0
summary_alphabet = [" ", "a", "b", "!"]
for length in range(7):
    for chars in itertools.product(summary_alphabet, repeat=length):
        value = "".join(chars)
        summary_case_count += 1
        summary = "".join(
            map(chr, anti_shuffle_summary(tuple(map(ord, value))))
        )
        if summary != canonical(value) or summary != candidate(value):
            summary_mismatches += 1
print(
    json.dumps(
        {
            "bounded_summary_bridge": {
                "alphabet": summary_alphabet,
                "lengths": [0, 1, 2, 3, 4, 5, 6],
                "cases": summary_case_count,
                "mismatches": summary_mismatches,
            }
        },
        sort_keys=True,
    )
)
if summary_mismatches:
    raise SystemExit(1)
