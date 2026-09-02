#!/usr/bin/env python3
"""Mechanical token-level comparison of submitted MPy AST and claim driver AST."""

from __future__ import annotations

import re
from pathlib import Path


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|'
    r"[A-Za-z_#][A-Za-z0-9_#-]*|"
    r"\.[A-Za-z][A-Za-z0-9]*|"
    r"=>|~>|//|"
    r"-?[0-9]+|"
    r"[(),+\-*/]"
)


def strip_line_comments(text: str) -> str:
    # Candidate K comments are full lines. Do not split on `//` because the
    # submitted constructor term contains the quoted floor-division operator.
    return "\n".join(
        "" if re.match(r"^\s*//", line) else line for line in text.splitlines()
    )


def tokens(text: str) -> list[str]:
    return TOKEN.findall(strip_line_comments(text))


def balanced_term(all_tokens: list[str], start: int) -> list[str]:
    if all_tokens[start] != "Module":
        raise ValueError("balanced term must begin with Module")
    depth = 0
    seen_open = False
    for end in range(start, len(all_tokens)):
        token = all_tokens[end]
        if token == "(":
            depth += 1
            seen_open = True
        elif token == ")":
            depth -= 1
            if seen_open and depth == 0:
                return all_tokens[start : end + 1]
    raise ValueError("unbalanced Module term")


submitted_text = Path(
    "/tmp/audit-work/115-max-fill-audit/solution.regenerated.mpy"
).read_text()
verification_text = Path(
    "/tmp/audit-work/115-max-fill-audit/verification.k"
).read_text()

submitted_tokens = tokens(submitted_text)
submitted_module = balanced_term(
    submitted_tokens, submitted_tokens.index("Module")
)

verification_tokens = tokens(verification_text)
driver_rule = verification_tokens.index("#runMaxFill", verification_tokens.index("rule"))
driver_module_start = verification_tokens.index("Module", driver_rule)
driver_module = balanced_term(verification_tokens, driver_module_start)

macro_lhs = verification_tokens.index(
    "MAX_FILL_LOOP_BODY", verification_tokens.index("rule")
)
macro_arrow = verification_tokens.index("=>", macro_lhs)
macro_end = verification_tokens.index("endmodule", macro_arrow)
macro_rhs = verification_tokens[macro_arrow + 1 : macro_end]

expanded_driver: list[str] = []
for token in driver_module:
    if token == "MAX_FILL_LOOP_BODY":
        expanded_driver.extend(macro_rhs)
    else:
        expanded_driver.append(token)

# `.Stmts` is the associative statement-list identity. The translator omits the
# textual identity while the macro includes it; deleting only this identity is
# the demonstrated inert normalization.
submitted_normalized = [token for token in submitted_module if token != ".Stmts"]
driver_normalized = [token for token in expanded_driver if token != ".Stmts"]

print(f"submitted_token_count={len(submitted_normalized)}")
print(f"driver_token_count={len(driver_normalized)}")
print(f"macro_rhs_tokens={macro_rhs}")
print(f"normalization=remove only .Stmts identity tokens")
print(f"constructor_tokens_equal={submitted_normalized == driver_normalized}")
if submitted_normalized != driver_normalized:
    for index, (left, right) in enumerate(
        zip(submitted_normalized, driver_normalized)
    ):
        if left != right:
            print(f"first_difference index={index} submitted={left!r} driver={right!r}")
            break
    print(f"submitted_normalized={submitted_normalized}")
    print(f"driver_normalized={driver_normalized}")
    raise SystemExit(1)
