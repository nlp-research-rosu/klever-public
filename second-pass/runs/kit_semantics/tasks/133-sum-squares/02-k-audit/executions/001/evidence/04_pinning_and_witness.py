#!/usr/bin/env python3
"""Independent constructor-level program pinning and concrete witnesses."""

from __future__ import annotations

import hashlib
import importlib.util
import math
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
program_k = (ROOT / "program.k").read_text()
solution_mpy = (ROOT / "solution.mpy").read_text()

assert program_k.count("syntax Module ::= \"solutionProgram\"") == 1
assert program_k.count("rule solutionProgram =>") == 1
assert "rule solutionProgram =>" in program_k
rule_rhs = program_k.split("rule solutionProgram =>", 1)[1].split(
    "endmodule", 1
)[0]

# Constructor-level comparison: whitespace and comments are inert here, while
# identifiers, quoted strings, integers, constructors, commas, and parentheses
# are all retained.
token_pattern = re.compile(
    r'"(?:\\.|[^"\\])*"|[A-Za-z_#][A-Za-z0-9_#-]*|-?[0-9]+|[(),]'
)
program_tokens = token_pattern.findall(rule_rhs)
translated_tokens = token_pattern.findall(solution_mpy)
assert program_tokens == translated_tokens
token_bytes = "\n".join(program_tokens).encode()
print(f"constructor_tokens={len(program_tokens)}")
print(f"constructor_token_sha256={hashlib.sha256(token_bytes).hexdigest()}")
print("solutionProgram_constructor_identity=true")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load(ROOT / "canonical.py", "canonical_ground")
generated = load(ROOT / "solution.py", "generated_ground")
for values in [[], [1, 2, 3], [1.4, -2.4, 0]]:
    mathematical = sum(math.ceil(value) ** 2 for value in values)
    trusted_result = canonical(values)
    generated_result = generated(values)
    assert mathematical == trusted_result == generated_result
    print(
        f"witness={values!r} fold={mathematical} "
        f"canonical={trusted_result} generated={generated_result}"
    )
