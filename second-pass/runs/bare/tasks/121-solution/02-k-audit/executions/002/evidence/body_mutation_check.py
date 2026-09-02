#!/usr/bin/env python3
"""Check that the mutated proof term equals the trusted translation of mutation."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, "/audit-output/evidence")
from program_pinning import constructor_term_after_rule, tokens


def main() -> int:
    scratch = Path("/tmp/audit-work/121-solution-audit")
    translated = tokens((scratch / "solution-operational-mutation.mpy").read_text())
    verification = (
        scratch / "body-mutation" / "verification-body-mutation.k"
    ).read_text()
    claimed = tokens(constructor_term_after_rule(verification, "solutionProgram"))
    original = tokens((scratch / "candidate" / "solution.mpy").read_text())
    print(f"mutation_translation_equals_executed_claim_term={translated == claimed}")
    print(f"mutation_executed_claim_term_differs_from_original={claimed != original}")
    return 0 if translated == claimed and claimed != original else 1


if __name__ == "__main__":
    sys.exit(main())
