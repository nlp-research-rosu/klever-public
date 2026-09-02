#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


for name, path in (
    ("canonical", Path("/tmp/audit-work/rebuild/canonical.py")),
    ("candidate", Path("/tmp/audit-work/rebuild/solution.py")),
):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    value = module.flip_case("é")
    print(name, repr(value), [ord(character) for character in value])
    assert value == "É"
print("PYTHON_MODEL_GAP_WITNESS=PASS")
