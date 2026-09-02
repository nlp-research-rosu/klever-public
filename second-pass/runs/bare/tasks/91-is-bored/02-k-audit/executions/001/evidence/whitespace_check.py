#!/usr/bin/env python3
"""Check the generated semantics' whitespace table against CPython 3.10."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
SEMANTICS = WORK / "semantic.k"
DEFINITION = WORK / "semantic-haskell-fresh-kompiled"

source = SEMANTICS.read_text(encoding="utf-8")
literal_texts = re.findall(
    r'^\s*rule whiteSpace\(("(?:\\.|[^"\\])*")\)\s*=>\s*true\s*$',
    source,
    flags=re.MULTILINE,
)
declared = {json.loads(literal) for literal in literal_texts}
python_whitespace = {
    chr(codepoint)
    for codepoint in range(sys.maxunicode + 1)
    if chr(codepoint).isspace()
}

print(f"python_version={sys.version.split()[0]}")
print(f"declared_count={len(declared)}")
print(f"cpython_isspace_count={len(python_whitespace)}")
print(f"missing_from_semantics={sorted(python_whitespace - declared)!r}")
print(f"extra_in_semantics={sorted(declared - python_whitespace)!r}")

spec = importlib.util.spec_from_file_location("ws_solution", WORK / "solution.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import submitted solution")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# One program input drives stripLeft and stripRight through every declared true
# rule, and also uses the owise false branch on the surrounding "I x".
aggregate = ".".join(char + "I x" + char for char in sorted(declared))
python_result = module.is_bored(aggregate)

command = [
    "krun",
    "solution.mpy",
    "--definition",
    str(DEFINITION),
    f"-cINPUT={json.dumps(aggregate)}",
    "--output",
    "pretty",
]
completed = subprocess.run(
    command,
    cwd=WORK,
    text=True,
    capture_output=True,
    check=False,
)
match = re.search(r"<result>\s*([0-9-]+)\s*</result>", completed.stdout)
if completed.returncode != 0 or match is None:
    raise RuntimeError(
        f"krun failed code={completed.returncode} "
        f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
    )
k_result = int(match.group(1))
print(f"COMMAND: {' '.join(command)}")
print(
    f"aggregate_segment_count={len(declared)} "
    f"submitted_python={python_result} K={k_result}"
)

ok = (
    declared == python_whitespace
    and python_result == len(declared)
    and k_result == python_result
)
raise SystemExit(0 if ok else 1)
