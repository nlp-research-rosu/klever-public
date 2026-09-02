#!/usr/bin/env python3
"""Create a body-sensitive mutation of the exact entry-claim program term."""

from __future__ import annotations

import re
from pathlib import Path


SOURCE = Path("/tmp/audit-work/candidate/spec.k")
OUTPUT = Path("/tmp/audit-work/candidate/spec-body-mutation.k")


def main() -> None:
    text = SOURCE.read_text()
    text = text.replace("module PLUCK-SPEC\n", "module PLUCK-SPEC-BODY-MUTATION\n", 1)
    text = text.replace("[pluck-correct]:", "[pluck-correct-body-mutation]:", 1)
    pattern = re.compile(
        r'ListExpr\(\s*Name\("smallest"\),\s*Name\("smallest_index"\)\)'
    )
    replacement = (
        'ListExpr(\n'
        '                BinOp("+", Name("smallest"), Int(1)),\n'
        '                Name("smallest_index"))'
    )
    text, count = pattern.subn(replacement, text)
    if count != 2:
        raise SystemExit(f"expected two executable/closure return terms, changed {count}")
    text = text.replace("endmodule\n", "endmodule\n", 1)
    OUTPUT.write_text(text)
    print(f"source={SOURCE}")
    print(f"output={OUTPUT}")
    print("mutation=both copies of entry-claim function body return smallest + 1")
    print(f"changed_program_terms={count}")
    print("BODY_MUTATION_GENERATION=PASS")


if __name__ == "__main__":
    main()
