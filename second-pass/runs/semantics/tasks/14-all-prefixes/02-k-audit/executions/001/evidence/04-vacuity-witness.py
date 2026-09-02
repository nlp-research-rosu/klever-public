#!/usr/bin/env python3
"""Ground witness for the deliberately false non-vacuity mutation."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.all_prefixes


canonical = load("/reference/canonical.py", "canonical_for_vacuity")
candidate = load(
    "/tmp/audit-work/proof-audit.Dl0nBZ/candidate/solution.py",
    "candidate_for_vacuity",
)
value = ""
real_canonical = canonical(value)
real_candidate = candidate(value)
false_required = [""] + real_candidate
print(
    json.dumps(
        {
            "input": value,
            "canonical": real_canonical,
            "candidate": real_candidate,
            "false_mutation_requires": false_required,
            "mutation_is_false": (
                real_canonical != false_required
                and real_candidate != false_required
            ),
        },
        sort_keys=True,
    )
)

