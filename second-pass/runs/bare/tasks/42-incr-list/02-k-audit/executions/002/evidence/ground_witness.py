#!/usr/bin/env python3
"""Evaluate the same satisfiable ground witness in both Python programs."""

import importlib.util
import json


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.incr_list


values = [1, 2]
canonical = load("/reference/canonical.py", "ground_canonical")
candidate = load("/tmp/audit-work/source/solution.py", "ground_candidate")
print(
    json.dumps(
        {
            "input": values,
            "trusted_canonical": canonical(list(values)),
            "generated_candidate": candidate(list(values)),
            "K_expected": "pyList(ListItem(pyInt(2)) ListItem(pyInt(3)))",
            "formal_claim_post": (
                "#incPrefix(ListItem(pyInt(1)) ListItem(pyInt(2)), 2)"
            ),
        },
        sort_keys=True,
    )
)
