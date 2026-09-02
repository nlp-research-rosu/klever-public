#!/usr/bin/env python3
import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pairs_sum_to_zero


root = Path("/tmp/audit-work")
canonical = load("canonical_witness", root / "canonical.py")
generated = load("generated_witness", root / "solution.py")

witnesses = [
    ("INPUT=.IntSeq", [], False),
    ("INPUT=iCons(0,.IntSeq)", [0], False),
    ("INPUT=iCons(5,iCons(-5,.IntSeq))", [5, -5], True),
    (
        "INPUT=iCons(2,iCons(4,iCons(-5,iCons(3,iCons(5,iCons(7,.IntSeq))))))",
        [2, 4, -5, 3, 5, 7],
        True,
    ),
    ("INPUT=iCons(1,iCons(2,iCons(3,.IntSeq)))", [1, 2, 3], False),
]

for formal, values, expected in witnesses:
    c = canonical(values.copy())
    g = generated(values.copy())
    assert c == expected and g == expected
    print(
        f"{formal} values={values!r} claimed={expected} "
        f"canonical={c} generated={g}"
    )
