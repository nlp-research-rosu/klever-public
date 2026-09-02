#!/usr/bin/env python3
"""Ground adequacy witnesses for the candidate's tagged-word abstraction."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.select_words


canonical = load(Path("/reference/canonical.py"), "canonical_stage4")
generated = load(Path("/tmp/audit-work/proof/solution.py"), "generated_stage4")

for s, n in [("", 0), ("b", 0), ("a", 0)]:
    print(
        f"python_input={s!r},n={n},"
        f"canonical={canonical(s, n)!r},generated={generated(s, n)!r}"
    )

print(
    "formal_keep_witness: "
    "N=0, WS=keepWord(codes('b'), .WordSeq) "
    "reduces selectedWords to ['b'] (wrapped as countedWord(0,codes('b')))"
)
print(
    "formal_skip_witness: "
    "N=0, WS=skipWord(codes('a'), .WordSeq) "
    "reduces selectedWords to [] while the projected real input is 'a'"
)
