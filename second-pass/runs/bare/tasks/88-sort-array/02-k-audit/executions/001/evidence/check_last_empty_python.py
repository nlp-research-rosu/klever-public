#!/usr/bin/env python3
"""Confirm CPython's result for the false-totalization witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path


path = Path("/audit-output/evidence/last_empty_probe.py")
spec = importlib.util.spec_from_file_location("last_empty_probe", path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load {path}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

try:
    module.sort_array([])
except IndexError as err:
    print(f"EXPECTED_EXCEPTION={type(err).__name__}: {err}")
else:
    raise AssertionError("empty-list [-1] unexpectedly returned a value")
