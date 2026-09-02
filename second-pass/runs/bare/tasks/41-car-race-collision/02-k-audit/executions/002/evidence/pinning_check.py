#!/usr/bin/env python3
"""Mechanically compare the claim's executed program constructor term to .mpy."""

from __future__ import annotations

import re
from pathlib import Path


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z][A-Za-z0-9-]*|-?[0-9]+|[(),]')


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


program_text = Path("/tmp/audit-work/candidate/solution.mpy").read_text()
spec_text = Path("/tmp/audit-work/candidate/spec.k").read_text()

program_tokens = tokens(program_text)
spec_k_prefix = spec_text.split("~>", 1)[0]
start = spec_k_prefix.index("Module(")
claim_program_tokens = tokens(spec_k_prefix[start:])

print("solution_token_count", len(program_tokens))
print("claim_program_token_count", len(claim_program_tokens))
print("solution_tokens", program_tokens)
print("claim_program_tokens", claim_program_tokens)
print("constructor_terms_equal", program_tokens == claim_program_tokens)

if program_tokens != claim_program_tokens:
    raise SystemExit(1)
