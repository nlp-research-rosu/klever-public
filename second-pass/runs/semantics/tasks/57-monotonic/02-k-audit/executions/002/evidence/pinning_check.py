#!/usr/bin/env python3
"""Mechanical source-to-claim constructor comparison and concrete claim witnesses."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.monotonic


def constructor_tokens(text: str) -> list[str]:
    # Constructor terms here contain identifiers, quoted strings, punctuation,
    # and no infix arithmetic. Keeping punctuation makes sequencing visible.
    return re.findall(r'"(?:[^"\\]|\\.)*"|[A-Za-z_][A-Za-z_0-9-]*|[(),]', text)


solution_text = Path("/candidate/solution.mpy").read_text()
verification_text = Path("/candidate/verification.k").read_text()

start = verification_text.index("rule monotonicProgram")
start = verification_text.index("=>", start) + 2
end = verification_text.index("// Independent", start)
claim_program_rhs = verification_text[start:end]

solution_tokens = constructor_tokens(solution_text)
claim_tokens = constructor_tokens(claim_program_rhs)
assert solution_tokens == claim_tokens, (
    f"program-term mismatch at token "
    f"{next(i for i, pair in enumerate(zip(solution_tokens, claim_tokens)) if pair[0] != pair[1])}"
)

print(f"solution_constructor_tokens={len(solution_tokens)}")
print(f"claim_constructor_tokens={len(claim_tokens)}")
print("constructor_level_program_identity=MATCH")

canonical = load_function("trusted_canonical_for_pinning", Path("/reference/canonical.py"))
candidate = load_function("candidate_for_pinning", Path("/candidate/solution.py"))


def nondecreasing(values):
    return all(left <= right for left, right in zip(values, values[1:]))


def nonincreasing(values):
    return all(left >= right for left, right in zip(values, values[1:]))


witnesses = [
    ("claim1-empty", []),
    ("claim1-nondecreasing", [1, 1, 3]),
    ("claim2-decreasing-true", [3, 2, 2, -1]),
    ("claim2-neither-false", [1, 3, 2]),
]
for name, values in witnesses:
    nd = nondecreasing(values)
    ni = nonincreasing(values)
    expected_claim_branch = True if nd else ni
    canonical_result = canonical(values)
    candidate_result = candidate(values)
    assert canonical_result == candidate_result == expected_claim_branch
    print(
        f"{name}: input={values!r} nondecreasing={nd} nonincreasing={ni} "
        f"formal_branch_result={expected_claim_branch} "
        f"canonical={canonical_result} candidate={candidate_result}"
    )

assert nondecreasing(witnesses[0][1])
assert nondecreasing(witnesses[1][1])
assert not nondecreasing(witnesses[2][1])
assert not nondecreasing(witnesses[3][1])
print("ENTRY_PRECONDITION_WITNESSES=SATISFIABLE")
print("PINNING_CHECK=PASS")
