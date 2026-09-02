#!/usr/bin/env python3
"""Independent Python expectations for the concrete K executions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_in_sentence


canonical = load("/reference/canonical.py", "concrete_canonical")
candidate = load("/tmp/audit-work/rebuild/solution.py", "concrete_candidate")

cases = {
    "example_1": "This is a test",
    "empty": "",
    "minimum_1": "a",
    "repeated_spaces": "  aa   bbb  ",
    "length_100_2_plus_97": "aa " + ("b" * 97),
    "length_100_composite": "c" * 100,
}

for label, sentence in cases.items():
    oracle = canonical(sentence)
    generated = candidate(sentence)
    print(
        json.dumps(
            {
                "label": label,
                "input": sentence,
                "input_length": len(sentence),
                "canonical": oracle,
                "candidate": generated,
                "match": oracle == generated,
            },
            sort_keys=True,
        )
    )
