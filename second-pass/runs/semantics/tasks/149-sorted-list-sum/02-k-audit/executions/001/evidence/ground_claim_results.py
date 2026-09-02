#!/usr/bin/env python3
"""Ground the entry claim's three heap values on satisfying list[str] inputs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


canonical = load(ROOT / "trusted" / "canonical.py", "ground_canonical")
submitted = load(ROOT / "solution.py", "ground_submitted")

cases = [
    [],
    ["a", "bb", "aa", "cccc"],
    ["zzzz", "aa", "bbbb", "cc", "x", "aa"],
]

for words in cases:
    heap_0_even_append = [word for word in words if len(word) % 2 == 0]
    heap_1_sort_vs = sorted(heap_0_even_append)
    heap_2_sort_key_vs = sorted(heap_1_sort_vs, key=len)
    record = {
        "input": words,
        "entry_precondition_witness": {
            "INPUT_is_StrList": True,
            "env": 0,
            "scopeLoc": 1,
            "heap": {},
            "heapLoc": 0,
            "stack": [],
            "ret": "noRet",
            "exc": "NoExc",
            "exit_code": 0,
        },
        "claimed_heap_0_evenAppend": heap_0_even_append,
        "claimed_heap_1_sortVS": heap_1_sort_vs,
        "claimed_heap_2_sortKeyVS": heap_2_sort_key_vs,
        "claimed_return_reference": 2,
        "canonical_return": canonical(list(words)),
        "submitted_return": submitted(list(words)),
    }
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    assert record["canonical_return"] == heap_2_sort_key_vs
    assert record["submitted_return"] == heap_2_sort_key_vs
