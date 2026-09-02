#!/usr/bin/env python3
"""Instantiate the entry claim's result recurrence on concrete witnesses."""

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
    return module.anti_shuffle


def insertion_sort(codes: list[int]) -> list[int]:
    result: list[int] = []
    for code in codes:
        index = len(result)
        while index > 0 and code < result[index - 1]:
            index -= 1
        result.insert(index, code)
    return result


def formal_scan(codes: list[int]) -> tuple[list[int], list[int]]:
    """Direct executable reading of scanOut/scanWord's equations."""
    output: list[int] = []
    word: list[int] = []
    for code in codes:
        if code == 32:
            output.extend(insertion_sort(word))
            output.append(32)
            word = []
        else:
            word.append(code)
    return output, word


canonical = load_entry(Path("/reference/canonical.py"), "canonical_substitution")
candidate = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "candidate_substitution"
)
witnesses = ["", "ba  c", "Hello World!!!"]

print(
    "entry_precondition="
    "#loadAll(exact submitted FuncDef) ~> Call(Name(\"anti_shuffle\"), str(CS)); "
    "env=0; empty module map and heap; builtinsScope; scopeLoc=1; heapLoc=0; "
    "empty stack; noRet; NoExc; exit-code=0"
)
for text in witnesses:
    codes = [ord(char) for char in text]
    scan_output, final_word = formal_scan(codes)
    formal_result_codes = scan_output + insertion_sort(final_word)
    formal_result = "".join(chr(code) for code in formal_result_codes)
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    record = {
        "CS": codes,
        "candidate": candidate_result,
        "canonical": canonical_result,
        "formal_antiShuffleCodes": formal_result_codes,
        "formal_text": formal_result,
        "input": text,
        "scanOut": scan_output,
        "scanWord": final_word,
    }
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    if not (formal_result == canonical_result == candidate_result):
        raise SystemExit(1)
