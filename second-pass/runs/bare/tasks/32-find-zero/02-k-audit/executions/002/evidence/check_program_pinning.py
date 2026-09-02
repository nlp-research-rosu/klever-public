#!/usr/bin/env python3
"""Mechanically compare the proof macro's constructor body with solution.mpy."""

from pathlib import Path
import re


verification = Path(
    "/tmp/audit-work/32-find-zero/verification.k"
).read_text(encoding="utf-8")
solution = Path(
    "/tmp/audit-work/32-find-zero/solution.mpy"
).read_text(encoding="utf-8")

match = re.search(
    r"rule\s+solution\s*=>\s*(Module\(.*?\)\)\))\s*"
    r"// Independent postcondition machinery",
    verification,
    flags=re.DOTALL,
)
assert match is not None
macro_body = match.group(1)


def constructor_tokens(text: str) -> list[str]:
    return re.findall(r'"(?:[^"\\]|\\.)*"|-?\d+|[A-Za-z_][A-Za-z_0-9]*|[(),]', text)


macro_tokens = constructor_tokens(macro_body)
solution_tokens = constructor_tokens(solution)
print(f"macro_token_count={len(macro_tokens)}")
print(f"solution_token_count={len(solution_tokens)}")
print(f"constructor_tokens_equal={macro_tokens == solution_tokens}")
if macro_tokens != solution_tokens:
    for index, (left, right) in enumerate(zip(macro_tokens, solution_tokens)):
        if left != right:
            print(f"first_difference={index}: macro={left!r} solution={right!r}")
            break
assert macro_tokens == solution_tokens
print("PROGRAM_PINNING_OK")
