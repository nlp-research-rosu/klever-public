#!/usr/bin/env python3
"""Check program-term pinning and concrete instances of the claim summary."""

from __future__ import annotations

import importlib.util
import math
import re
import subprocess
from pathlib import Path

WORK = Path("/tmp/audit-work/audit147")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


program = (WORK / "regenerated-solution.mpy").read_text(encoding="utf-8")
spec_text = (WORK / "spec.k").read_text(encoding="utf-8")
match = re.search(r"<k>\s*(Module\(.*?\))\s*=>\s*\.K\s*</k>", spec_text, re.DOTALL)
if match is None:
    raise SystemExit("could not extract entry claim program term")
claim_program = match.group(1)
program_term_match = compact(program) == compact(claim_program)

canonical = load_entry(Path("/reference/canonical.py"), "canonical_for_claim")
generated = load_entry(WORK / "solution.py", "generated_for_claim")


def valid_triple_count(n: int) -> int:
    zero_residue_count = (n + 1) // 3
    one_residue_count = n - zero_residue_count
    return math.comb(zero_residue_count, 3) + math.comb(one_residue_count, 3)


inputs = [1, 2, 3, 4, 5, 10, 31]
mismatches = []
for n in inputs:
    command = [
        "krun",
        str(WORK / "regenerated-solution.mpy"),
        "--definition",
        str(WORK / "fresh-runtime-kompiled"),
        f"-cN={n}",
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    output = completed.stdout + completed.stderr
    result_match = re.search(
        r"<result>\s*result\s*\(\s*(-?\d+)\s*\)\s*</result>", output
    )
    k_value = int(result_match.group(1)) if result_match else None
    summary = valid_triple_count(n)
    oracle = canonical(n)
    implementation = generated(n)
    print(
        f"N={n} satisfies_precondition={n >= 1} "
        f"claim_summary={summary} K={k_value} "
        f"canonical={oracle} generated={implementation}"
    )
    if (
        completed.returncode != 0
        or not (summary == k_value == oracle == implementation)
    ):
        mismatches.append(n)

print(f"claim_program_matches_regenerated_solution_mpy={program_term_match}")
print("satisfying_entry_state_example=N=5, env=.Map, result=noResult")
print("N=5 summary=choose3(2)+choose3(3)=0+1=1")
print(f"mismatch_count={len(mismatches)}")
if not program_term_match or mismatches:
    raise SystemExit(1)
print("RESULT=PASS")
