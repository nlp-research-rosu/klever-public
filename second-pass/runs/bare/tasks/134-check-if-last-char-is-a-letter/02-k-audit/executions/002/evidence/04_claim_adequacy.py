#!/usr/bin/env python3
"""Concrete precondition witnesses and postcondition substitutions."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


canonical = load(Path("/reference/canonical.py"), "adequacy_canonical")
submitted = load(Path("/tmp/audit-work/task134/solution.py"), "adequacy_submitted")

def k_result(text: str) -> bool:
    encoded = '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'
    result = subprocess.run(
        [
            "krun",
            "solution.mpy",
            "--definition",
            "verification-audit-kompiled",
            f"-cTXT={encoded}",
        ],
        cwd="/tmp/audit-work/task134",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    if "pyBool ( true )" in result.stdout:
        return True
    if "pyBool ( false )" in result.stdout:
        return False
    raise AssertionError(result.stdout)


witnesses = ["", "A", "7", "ab", " a", "apple pi e", "é", " é", "界"]
print("ENTRY_PRECONDITION=any K String S; no requires clause")
print("Each listed Python string parses as the configuration variable TXT and hence")
print("exhibits a realizable entry state with the exact claim-program term.")
for text in witnesses:
    k = k_result(text)
    c = canonical(text)
    s = submitted(text)
    print(
        f"WITNESS {text!r}: claimed/K={k!r}, "
        f"trusted_canonical={c!r}, submitted_python={s!r}"
    )

assert k_result("A") is True
assert k_result("7") is False
assert k_result("é") is False
assert submitted("é") is True
assert canonical("é") is False
print("ADEQUACY_WITNESS='é': theorem conclusion false, real submitted program true")
