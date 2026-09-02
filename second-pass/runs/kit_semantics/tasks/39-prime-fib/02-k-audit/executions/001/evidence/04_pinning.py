#!/usr/bin/env python3
"""Mechanically compare the proof macro body with trusted translation output."""

from __future__ import annotations

import json
import re
import shlex
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/39-prime-fib-audit")
verification = (ROOT / "verification.k").read_text()
spec = (ROOT / "spec.k").read_text()


def macro_rhs(name: str) -> str:
    pattern = re.compile(
        rf"(?ms)^\s*rule\s+{re.escape(name)}\s*\n?\s*=>\s*(.*?)(?=^\s*rule\s+|^endmodule)"
    )
    match = pattern.search(verification)
    if match is None:
        raise AssertionError(f"missing macro rule {name}")
    rhs = match.group(1)
    rhs = rhs.split("\n  //", 1)[0].strip()
    return rhs


def lexical_tokens(text: str) -> list[str]:
    return re.findall(r'"(?:[^"\\]|\\.)*"|#?[A-Za-z_][A-Za-z0-9_]*|-?\d+|[(),.+*%<>=]+', text)


inner = macro_rhs("primeFibInner")
inner_core = macro_rhs("primeFibInnerCore")
outer = macro_rhs("primeFibOuter")
outer_core = macro_rhs("primeFibOuterCore")
body = macro_rhs("primeFibBody")

assert lexical_tokens(inner) == lexical_tokens(inner_core.replace("#while", "While"))
assert lexical_tokens(outer) == lexical_tokens(outer_core.replace("#while", "While"))
print("inner source-loop macro == inner #while anchor after constructor substitution: MATCH")
print("outer source-loop macro == outer #while anchor after constructor substitution: MATCH")

expanded_outer = re.sub(r"\bprimeFibInner\b", inner, outer)
expanded_body = re.sub(r"\bprimeFibOuter\b", expanded_outer, body)
# .Stmts is K's explicit list unit in rule syntax; an empty program-list slot
# is represented by omission in the external .mpy parser.
expanded_program_text = expanded_body.replace(".Stmts", "")
expanded_path = ROOT / "04_macrobody_expanded.txt"
expanded_path.write_text(expanded_program_text + "\n")

definition = ROOT / "verification-audit-kompiled"
commands = [
    [
        "kast",
        "solution.regenerated.mpy",
        "--definition",
        str(definition),
        "--module",
        "VERIFICATION-SYNTAX",
        "--sort",
        "Module",
        "--output",
        "json",
    ],
    [
        "kast",
        str(expanded_path),
        "--definition",
        str(definition),
        "--module",
        "VERIFICATION-SYNTAX",
        "--sort",
        "Stmts",
        "--output",
        "json",
    ],
]
outputs = []
for command in commands:
    print("$", shlex.join(command))
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    print(f"[exit {result.returncode}]")
    if result.stderr:
        print(result.stderr, end="")
    if result.returncode:
        raise SystemExit(result.returncode)
    outputs.append(json.loads(result.stdout))

module_term = outputs[0]["term"]
translated_body = module_term["args"][0]["args"][0]["args"][2]
macro_body = outputs[1]["term"]
assert translated_body == macro_body
print("trusted-regenerated FuncDef body == recursively expanded primeFibBody: MATCH")

entry_pattern = re.compile(
    r'Call\(Name\("prime_fib"\),\s*\(Int\(N\),\s*\.Exprs\)\).*?'
    r'"prime_fib"\s*\|->\s*closureVal\("n",\s*primeFibBody,\s*0\)',
    re.S,
)
assert entry_pattern.search(spec)
print("entry claim binds Call(Name(\"prime_fib\"), Int(N)) to closureVal(\"n\", primeFibBody, 0): MATCH")
