#!/usr/bin/env python3
import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_string


canonical = load(Path("/reference/canonical.py"), "canonical_ground")
generated = load(
    Path("/tmp/audit-work/101-words-string-independent-audit/solution.py"),
    "generated_ground",
)

for source, formal_result in [("", []), ("a,b", ["a", "b"])]:
    oracle = canonical(source)
    subject = generated(source)
    assert formal_result == oracle == subject
    print(
        f"input={source!r} formal={formal_result!r} "
        f"canonical={oracle!r} generated={subject!r}"
    )
