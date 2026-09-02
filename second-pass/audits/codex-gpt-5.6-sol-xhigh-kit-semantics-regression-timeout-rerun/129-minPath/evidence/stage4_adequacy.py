#!/usr/bin/env python3
"""Independent claim-witness and proof-program identity checks."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "audit-verification-kompiled"


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def extract_balanced_funcdef(source: str) -> str:
    marker = "rule MinPathDefinition"
    marker_at = source.index(marker)
    arrow_at = source.index("=>", marker_at)
    start = source.index("FuncDef", arrow_at)
    depth = 0
    quoted = False
    escaped = False
    for end in range(start, len(source)):
        char = source[end]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return source[start : end + 1]
    raise RuntimeError("unterminated MinPathDefinition RHS")


def parse_program(path: Path) -> Any:
    completed = subprocess.run(
        [
            "kast",
            "--definition",
            str(DEFINITION),
            "--input",
            "program",
            "--output",
            "json",
            str(path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"kast failed for {path}: exit={completed.returncode}\n{completed.stderr}"
        )
    return json.loads(completed.stdout)["term"]


def main() -> int:
    verification = (WORK / "verification.k").read_text(encoding="utf-8")
    rhs = extract_balanced_funcdef(verification)
    # External MPY program syntax uses empty argument positions for these units.
    rhs_program = rhs.replace(".Stmts", "").replace(".Exprs", "")
    embedded_program = f"Module({rhs_program})\n"

    solution_text = (WORK / "solution.mpy").read_text(encoding="utf-8")
    mutation_old = 'Attribute(Name("result"), "append"), Int(1)'
    mutation_new = 'Attribute(Name("result"), "append"), Int(9)'
    if solution_text.count(mutation_old) != 1:
        raise RuntimeError("body-sensitivity mutation site is not unique")
    mutated_solution = solution_text.replace(mutation_old, mutation_new)

    with tempfile.TemporaryDirectory(dir="/tmp/audit-work") as directory:
        temporary = Path(directory)
        embedded_path = temporary / "embedded.mpy"
        mutated_path = temporary / "mutated-solution.mpy"
        embedded_path.write_text(embedded_program, encoding="utf-8")
        mutated_path.write_text(mutated_solution, encoding="utf-8")
        submitted_ast = parse_program(WORK / "solution.mpy")
        embedded_ast = parse_program(embedded_path)
        mutated_ast = parse_program(mutated_path)

    exact_match = submitted_ast == embedded_ast
    mutation_detected = mutated_ast != embedded_ast
    print(f"submitted_solution_ast_equals_proof_macro={exact_match}")
    print(f"body_mutation_detected_by_identity_check={mutation_detected}")

    canonical = load_entry(Path("/reference/canonical.py"), "canonical_stage4")
    generated = load_entry(WORK / "solution.py", "generated_stage4")
    cases = [
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            3,
            [1, 2, 1],
        ),
        (
            [[5, 9, 3], [4, 1, 6], [7, 8, 2]],
            1,
            [1],
        ),
        (
            [[5, 9, 3], [4, 1, 6], [7, 8, 2]],
            6,
            [1, 4, 1, 4, 1, 4],
        ),
        (
            [[4, 3], [2, 1]],
            5,
            [1, 2, 1, 2, 1],
        ),
    ]
    witnesses = []
    all_match = True
    for grid, k, claimed in cases:
        canonical_result = canonical([row[:] for row in grid], k)
        generated_result = generated([row[:] for row in grid], k)
        matches = canonical_result == generated_result == claimed
        all_match = all_match and matches
        witnesses.append(
            {
                "grid": grid,
                "k": k,
                "claimed": claimed,
                "canonical": canonical_result,
                "generated": generated_result,
                "matches": matches,
            }
        )
    print("ground_claim_witnesses=" + json.dumps(witnesses, sort_keys=True))
    print(f"all_ground_claim_results_match={all_match}")
    return 0 if exact_match and mutation_detected and all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
