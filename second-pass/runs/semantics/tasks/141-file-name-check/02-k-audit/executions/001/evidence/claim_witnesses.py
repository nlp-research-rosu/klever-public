#!/usr/bin/env python3
"""Concrete satisfiability witnesses for the six entry-claim preconditions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


canonical = load_entry(Path("/reference/canonical.py"), "canonical_witness")
candidate = load_entry(
    Path("/tmp/audit-work/141-file-name-check/solution.py"), "candidate_witness"
)


def observations(text: str):
    suffix = text[-4:]
    return {
        "IntSeq": [ord(ch) for ch in text],
        "charCount(dot)": text.count("."),
        "isLen": len(text),
        "headCode": ord(text[0]) if text else None,
        "latinCode(headCode)": bool(text)
        and ("A" <= text[0] <= "Z" or "a" <= text[0] <= "z"),
        "suffix4": suffix,
        "suffixIs(txt,exe,dll)": [
            suffix == ".txt",
            suffix == ".exe",
            suffix == ".dll",
        ],
        "allowedSuffix": suffix in {".txt", ".exe", ".dll"},
        "digitCount": sum("0" <= ch <= "9" for ch in text),
    }


witnesses = [
    ("reject-dot-count", "abc.txt.txt", "No"),
    ("reject-short", ".txt", "No"),
    ("reject-first", "1.txt", "No"),
    ("reject-suffix", "a.pdf", "No"),
    ("reject-digits", "a1234.txt", "No"),
    ("accept", "a123.txt", "Yes"),
]

for claim, text, claimed in witnesses:
    row = {
        "claim": claim,
        "input": text,
        "formal_observations_under_intended_interpretation": observations(text),
        "claimed_result": claimed,
        "canonical_result": canonical(text),
        "candidate_result": candidate(text),
        "shared_initial_state": {
            "env": 0,
            "scope0": "scope(.Map, parent(-1))",
            "scope-1": "builtinsScope",
            "scopeLoc": 1,
            "heap": ".Map",
            "heapLoc": 0,
            "stack": ".List",
            "ret": "noRet",
            "exc": "NoExc",
            "exit-code": 0,
        },
    }
    print(json.dumps(row, ensure_ascii=False, sort_keys=True))
    if row["canonical_result"] != claimed or row["candidate_result"] != claimed:
        raise SystemExit(f"witness result mismatch: {claim}")
