#!/usr/bin/env python3
"""Independent token-level comparison of trusted .mpy and solutionProgram."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path("/tmp/audit-work/118-get-closest-vowel")
MPY = ROOT / "trusted-regenerated.mpy"
PROGRAM = ROOT / "candidate-src" / "program.k"

TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|\.Stmts|[A-Za-z][A-Za-z0-9_-]*|-?[0-9]+|[(),]'
)


def main() -> int:
    mpy_text = MPY.read_text(encoding="utf-8")
    program_text = PROGRAM.read_text(encoding="utf-8")
    header = (
        'module SOLUTION-PROGRAM\n'
        '  imports MPY-SYNTAX\n'
        '  syntax Module ::= "solutionProgram" [function]\n'
        '  rule solutionProgram =>\n'
    )
    assert program_text.startswith(header)
    assert program_text.endswith("endmodule\n")
    rhs = program_text[len(header) : -len("endmodule\n")]
    mpy_tokens = TOKEN.findall(mpy_text)
    program_tokens = TOKEN.findall(rhs)
    explicit_empty_lists = program_tokens.count(".Stmts")
    program_without_units = [
        token for token in program_tokens if token != ".Stmts"
    ]
    same = program_without_units == mpy_tokens
    print(f"trusted_mpy={MPY}")
    print(f"program_module={PROGRAM}")
    print(f"trusted_mpy_token_count={len(mpy_tokens)}")
    print(f"program_rhs_token_count={len(program_tokens)}")
    print(f"explicit_empty_Stmt_units={explicit_empty_lists}")
    print(f"constructor_tokens_equal_after_empty_units={same}")
    print(f"solutionProgram_occurrences={program_text.count('solutionProgram')}")
    return 0 if same and program_text.count("solutionProgram") == 2 else 1


if __name__ == "__main__":
    sys.exit(main())
