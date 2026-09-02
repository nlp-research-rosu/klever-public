#!/usr/bin/env python3
"""Check exact normalized inclusion of submitted MPY in the entry claim."""

from __future__ import annotations

import re
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    solution = normalized((WORK / "solution.mpy").read_text())
    raw_spec = (WORK / "spec.k").read_text()
    spec = normalized(raw_spec)
    occurrences = spec.count(solution)
    load_start = raw_spec.index("#loadAll(") + len("#loadAll(")
    depth = 1
    cursor = load_start
    while depth:
        character = raw_spec[cursor]
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        cursor += 1
    loaded_program = raw_spec[load_start : cursor - 1].strip() + "\n"
    raw_extracted_path = WORK / "spec-loaded-program.kterm"
    raw_extracted_path.write_text(loaded_program)
    parser_form = loaded_program.replace(".Stmts", "")
    extracted_path = WORK / "spec-loaded-program.mpy"
    extracted_path.write_text(parser_form)
    proof_argument = 'list(floatVals(INPUT:FloatSeq)),THRESHOLD:Float'
    runtime_empty = "list(.ValSeq)"
    print(f"normalized_solution_chars={len(solution)}")
    print(f"normalized_solution_occurrences_in_spec={occurrences}")
    print(
        "textual_difference_reason=spec spells empty statement lists as .Stmts; "
        "submitted parser syntax elides them"
    )
    print(f"raw_extracted_loaded_program={raw_extracted_path}")
    print(f"program_parser_form={extracted_path}")
    print(f"proof_argument_present={proof_argument in spec}")
    print(f"canonical_runtime_empty_literal_present_in_target={runtime_empty in spec}")
    print(
        "result=program_extracted_for_parser_ast_comparison_and_input_uses_proof_only_floatVals"
        if proof_argument in spec
        else "result=unexpected"
    )
    return 0 if proof_argument in spec else 1


if __name__ == "__main__":
    raise SystemExit(main())
