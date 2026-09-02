#!/usr/bin/env python3
"""Constructor-level comparison of solution.mpy and solutionProgram's RHS."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
TOKEN = re.compile(r'\s*(?:(-?\d+)|("(?:[^"\\]|\\.)*")|([A-Za-z_.][A-Za-z0-9_.]*)|(.))')


class Parser:
    def __init__(self, text: str):
        self.tokens: list[object] = []
        for match in TOKEN.finditer(text):
            integer, string, identifier, punctuation = match.groups()
            if integer is not None:
                self.tokens.append(int(integer))
            elif string is not None:
                self.tokens.append(json.loads(string))
            elif identifier is not None:
                self.tokens.append(identifier)
            elif punctuation in {"(", ")", ","}:
                self.tokens.append(punctuation)
            else:
                raise ValueError(f"unexpected token {punctuation!r}")
        self.index = 0

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def take(self, wanted=None):
        value = self.peek()
        if wanted is not None and value != wanted:
            raise ValueError(f"wanted {wanted!r}, got {value!r} at token {self.index}")
        self.index += 1
        return value

    def parse_program(self):
        self.take("Module")
        self.take("(")
        body = self.parse_statements({")"})
        self.take(")")
        if self.peek() is not None:
            raise ValueError(f"trailing token {self.peek()!r}")
        return ("Module", tuple(body))

    def parse_statements(self, terminators):
        if self.peek() == ".Stmts":
            self.take(".Stmts")
            return []
        statements = []
        while self.peek() not in terminators:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        constructor = self.take()
        self.take("(")
        if constructor == "FuncDef":
            name = self.take()
            self.take(",")
            params = self.parse_params()
            self.take(",")
            body = self.parse_statements({")"})
            self.take(")")
            return ("FuncDef", name, params, tuple(body))
        if constructor == "Assign":
            target = self.parse_expr()
            self.take(",")
            value = self.parse_expr()
            self.take(")")
            return ("Assign", target, value)
        if constructor == "If":
            condition = self.parse_expr()
            self.take(",")
            then = self.parse_statements({","})
            self.take(",")
            otherwise = self.parse_statements({")"})
            self.take(")")
            return ("If", condition, tuple(then), tuple(otherwise))
        if constructor == "Return":
            value = self.parse_expr()
            self.take(")")
            return ("Return", value)
        raise ValueError(f"unexpected statement constructor {constructor!r}")

    def parse_params(self):
        self.take("Params")
        self.take("(")
        name = self.take()
        self.take(")")
        return ("Params", name)

    def parse_expr(self):
        constructor = self.take()
        self.take("(")
        if constructor == "Int":
            value = self.take()
            self.take(")")
            return ("Int", value)
        if constructor == "Name":
            value = self.take()
            self.take(")")
            return ("Name", value)
        if constructor == "BinOp":
            operator = self.take()
            self.take(",")
            left = self.parse_expr()
            self.take(",")
            right = self.parse_expr()
            self.take(")")
            return ("BinOp", operator, left, right)
        if constructor == "Compare":
            left = self.parse_expr()
            self.take(",")
            comparison = self.parse_cmpop()
            self.take(")")
            return ("Compare", left, comparison)
        if constructor == "TupleExpr":
            left = self.parse_expr()
            self.take(",")
            right = self.parse_expr()
            self.take(")")
            return ("TupleExpr", left, right)
        raise ValueError(f"unexpected expression constructor {constructor!r}")

    def parse_cmpop(self):
        self.take("CmpOp")
        self.take("(")
        operator = self.take()
        self.take(",")
        right = self.parse_expr()
        self.take(")")
        return ("CmpOp", operator, right)


translated_text = (WORK / "solution.mpy").read_text()
verification_text = (WORK / "verification.k").read_text()
start = verification_text.index("rule solutionProgram =>") + len("rule solutionProgram =>")
end = verification_text.index("// Independent reference model:")
alias_text = verification_text[start:end].strip()

translated = Parser(translated_text).parse_program()
alias = Parser(alias_text).parse_program()
translated_json = json.dumps(translated, separators=(",", ":"))
alias_json = json.dumps(alias, separators=(",", ":"))

print("COMMAND: python3 /audit-output/evidence/program_term_compare.py")
print("normalization=constructor parse; empty translated statement lists normalize to .Stmts")
print(f"translated_ast_sha256={hashlib.sha256(translated_json.encode()).hexdigest()}")
print(f"solutionProgram_ast_sha256={hashlib.sha256(alias_json.encode()).hexdigest()}")
print(f"constructor_ast_equal={translated == alias}")
if translated != alias:
    print(f"translated_ast={translated_json}")
    print(f"solutionProgram_ast={alias_json}")
raise SystemExit(0 if translated == alias else 1)
