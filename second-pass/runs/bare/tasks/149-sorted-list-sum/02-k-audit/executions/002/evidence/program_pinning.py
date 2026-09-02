#!/usr/bin/env python3
"""Mechanical source-to-claim program-term identity check."""

from __future__ import annotations

import hashlib
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    translated = (SCRATCH / "regenerated-solution.mpy").read_text(
        encoding="utf-8"
    ).strip()
    # These are K surface spellings of the empty units of the two list sorts.
    normalized = translated.replace("CellVars()", "CellVars(.Strings)")
    normalized = normalized.replace("FreeVars()", "FreeVars(.Strings)")
    normalized = "\n".join("    " + line for line in normalized.splitlines())

    program_source = (SCRATCH / "solution-program.k").read_text(encoding="utf-8")
    marker = "  rule solutionProgram =>\n"
    if program_source.count(marker) != 1 or not program_source.endswith("endmodule\n"):
        raise RuntimeError("unexpected solution-program.k structure")
    program_rhs = program_source.split(marker, 1)[1].rsplit("\nendmodule\n", 1)[0]

    spec_source = (SCRATCH / "spec.k").read_text(encoding="utf-8")
    claim_count = spec_source.count("claim <k>")
    solution_program_uses = spec_source.count("Run(solutionProgram,")

    print(f"trusted_translated_term_sha256={digest(translated)}")
    print(f"normalized_program_rhs_sha256={digest(normalized)}")
    print(f"submitted_program_rhs_sha256={digest(program_rhs)}")
    print(f"constructor_level_equal={normalized == program_rhs}")
    print("normalizations=CellVars()->CellVars(.Strings),FreeVars()->FreeVars(.Strings)")
    print(f"entry_claims={claim_count}")
    print(f"entry_claims_using_solutionProgram={solution_program_uses}")
    print(f"all_entry_claims_pinned={claim_count == solution_program_uses == 7}")
    if normalized != program_rhs or claim_count != solution_program_uses:
        return 1
    print("PROGRAM_PINNING_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
