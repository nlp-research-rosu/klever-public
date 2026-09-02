#!/usr/bin/env python3
"""Constructor-level comparison of solution.mpy and solutionProgram's RHS."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys


WORK = Path("/tmp/audit-work/35-max-element")


TOKEN = re.compile(r'\s*(?:(?P<name>[A-Za-z][A-Za-z0-9-]*)|(?P<string>"(?:\\.|[^"])*")|(?P<punct>[(),]))')


class Parser:
    def __init__(self, text: str):
        self.tokens = []
        pos = 0
        while pos < len(text):
            match = TOKEN.match(text, pos)
            if not match:
                if text[pos:].strip() == "":
                    break
                raise ValueError(f"unparsed constructor text at offset {pos}: {text[pos:pos+60]!r}")
            self.tokens.append(match.group(match.lastgroup))
            pos = match.end()
        self.index = 0

    def pop(self) -> str:
        token = self.tokens[self.index]
        self.index += 1
        return token

    def parse(self):
        name = self.pop()
        if self.index >= len(self.tokens) or self.tokens[self.index] != "(":
            if name.startswith('"'):
                return ("String", json.loads(name))
            return ("Atom", name)
        self.pop()
        args = []
        if self.tokens[self.index] != ")":
            while True:
                args.append(self.parse())
                if self.tokens[self.index] == ",":
                    self.pop()
                    continue
                break
        assert self.pop() == ")"
        return ("Ctor", name, tuple(args))

    def all(self):
        term = self.parse()
        if self.index != len(self.tokens):
            raise ValueError(f"unused tokens: {self.tokens[self.index:]}")
        return term


def verification_rhs(text: str) -> str:
    match = re.search(
        r"rule\s+solutionProgram\s*=>\s*(Module\s*\(.*?\)\s*\)\s*\))\s*\n\s*\n",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError("could not extract solutionProgram rule RHS")
    return match.group(1)


def digest(term) -> str:
    encoded = json.dumps(term, separators=(",", ":"), sort_keys=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    submitted_text = (WORK / "solution.mpy").read_text()
    rule_text = verification_rhs((WORK / "verification.k").read_text())
    submitted = Parser(submitted_text).all()
    rule_rhs = Parser(rule_text).all()
    equal = submitted == rule_rhs
    print(
        json.dumps(
            {
                "submitted_source": str(WORK / "solution.mpy"),
                "claim_constructor_source": str(WORK / "verification.k"),
                "submitted_term": submitted,
                "claim_rule_rhs_term": rule_rhs,
                "submitted_term_sha256": digest(submitted),
                "claim_rule_rhs_term_sha256": digest(rule_rhs),
                "constructor_terms_equal": equal,
            },
            indent=2,
        )
    )
    return 0 if equal else 1


if __name__ == "__main__":
    sys.exit(main())
