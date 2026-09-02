#!/usr/bin/env python3
"""Show that the body mutation changes the exact K term and a real result."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z0-9_-]*|-?[0-9]+|[(),]')


def tokens(text: str) -> list[str]:
    parsed = TOKEN.findall(text)
    assert TOKEN.sub("", text).strip() == ""
    return parsed


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


work = Path("/tmp/audit-work/rebuild")
base = tokens((work / "solution.mpy").read_text())
mutated = tokens((work / "solution-body-mutated.mpy").read_text())
mutated_spec = (work / "spec-body-mutated.k").read_text()
mutated_claim = tokens(mutated_spec.split("<k>", 1)[1].split("=> .K", 1)[0])

assert mutated == mutated_claim
assert base != mutated
differences = [
    (index, original, changed)
    for index, (original, changed) in enumerate(zip(base, mutated))
    if original != changed
]
assert len(differences) == 1
assert differences[0][1:] == ('"+"', '"-"')

original_entry = load_entry("body_original", work / "solution.py")
mutated_entry = load_entry("body_changed", work / "solution-body-mutated.py")
assert original_entry(5) == 1
assert mutated_entry(5) == -1

print("constructor-token differences:", differences)
print("mutated translation equals mutated claim term: PASS")
print("ground sensitivity witness: N=5 original=1 mutated=-1 target=1")
print("BODY TERM SENSITIVITY PRECHECK: PASS")
