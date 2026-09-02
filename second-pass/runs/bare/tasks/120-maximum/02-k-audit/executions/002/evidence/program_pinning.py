#!/usr/bin/env python3
"""Mechanical token comparison of translated module and entry-claim program term."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/120-maximum")
MPY = ROOT / "candidate" / "solution.mpy"
SPEC = ROOT / "candidate" / "spec.k"

TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z0-9_-]*|-?[0-9]+|[(),]')


def tokens(text: str) -> list[str]:
    found = TOKEN.findall(text)
    residual = TOKEN.sub("", text)
    if residual.strip():
        raise ValueError(f"unrecognized non-whitespace text: {residual!r}")
    return found


def digest(items: list[str]) -> str:
    return hashlib.sha256("\0".join(items).encode()).hexdigest()


def main() -> None:
    translated_text = MPY.read_text()
    spec_text = SPEC.read_text()
    k_start = spec_text.index("<k>") + len("<k>")
    boot = spec_text.index("~> boot", k_start)
    claim_program_text = spec_text[k_start:boot]

    translated_tokens = tokens(translated_text)
    claim_tokens = tokens(claim_program_text)
    equal = translated_tokens == claim_tokens
    print(f"translated_sha256={hashlib.sha256(translated_text.encode()).hexdigest()}")
    print(f"translated_token_count={len(translated_tokens)}")
    print(f"translated_token_sha256={digest(translated_tokens)}")
    print(f"claim_program_token_count={len(claim_tokens)}")
    print(f"claim_program_token_sha256={digest(claim_tokens)}")
    print(f"constructor_token_identity={equal}")
    if not equal:
        for index, pair in enumerate(zip(translated_tokens, claim_tokens)):
            if pair[0] != pair[1]:
                print(f"first_difference={index}: translated={pair[0]!r} claim={pair[1]!r}")
                break
        raise SystemExit(1)


if __name__ == "__main__":
    main()
