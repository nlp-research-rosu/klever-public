#!/usr/bin/env python3
"""Exhibit satisfying claim states and compare concrete claimed results."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


canonical = load_function("canonical_witness", Path("/reference/canonical.py"))
generated = load_function(
    "generated_witness", Path("/tmp/audit-work/reconstruction/solution.py")
)


def k_summary(text: str, depth: int = 0) -> bool:
    if not text:
        return depth == 0
    if depth < 0:
        return False
    head, rest = text[0], text[1:]
    if depth == 0 and head != "<":
        return False
    return k_summary(rest, depth + 1 if head == "<" else depth - 1)


print(
    "entry_witness: S=.IntSeq; initial env=0, module scope=empty, "
    "heap/stack empty, ret=noRet, exc=NoExc"
)
print(
    "loop_zero_witness: input='', suffix='', L=1, depth=0, "
    "bracket='', caller=0, saved=1, SC has only module/builtin frames"
)
print(
    "loop_positive_witness: input='<>', suffix='>', L=1, depth=1, "
    "bracket='<', caller=0, saved=1, SC has only module/builtin frames"
)
for text in ("", "<", "<>", "><"):
    formal = k_summary(text)
    trusted = canonical(text)
    submitted = generated(text)
    print(
        f"input={text!r} bracketResult={formal} "
        f"canonical={trusted} submitted={submitted}"
    )
    assert formal == trusted == submitted
