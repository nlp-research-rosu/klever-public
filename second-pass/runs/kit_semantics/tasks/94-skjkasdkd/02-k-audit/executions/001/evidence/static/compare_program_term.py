#!/usr/bin/env python3
"""Mechanically compare the submitted MPY body with expanded K body aliases."""

import hashlib
import re
from pathlib import Path


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|=>|>=|<=|==|!=|//|'
    r'[A-Za-z_#?.][A-Za-z0-9_#?.-]*|-?[0-9]+|[(),%+<>]'
)


def tokens(text: str) -> list[str]:
    without_comment_lines = "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("//")
    )
    return TOKEN.findall(without_comment_lines)


def third_argument_of_funcdef(text: str) -> list[str]:
    stream = tokens(text)
    start = stream.index("FuncDef")
    assert stream[start + 1] == "("
    depth = 1
    commas = []
    end = None
    for index in range(start + 2, len(stream)):
        if stream[index] == "(":
            depth += 1
        elif stream[index] == ")":
            depth -= 1
            if depth == 0:
                end = index
                break
        elif stream[index] == "," and depth == 1:
            commas.append(index)
    assert end is not None and len(commas) == 2
    return stream[commas[1] + 1 : end]


verification = Path("/candidate/verification.k").read_text()
definitions: dict[str, list[str]] = {}
for name in ("primeLoopBody", "scanBody", "digitLoopBody", "targetBody"):
    match = re.search(
        rf"^\s*rule\s+{name}\s*\n?\s*=>\s*(.*?)(?=^\s*(?:syntax|rule|endmodule)\b)",
        verification,
        re.MULTILINE | re.DOTALL,
    )
    assert match, name
    definitions[name] = tokens(match.group(1))


def expand(stream: list[str]) -> list[str]:
    output: list[str] = []
    for token in stream:
        if token in definitions:
            output.extend(expand(definitions[token]))
        elif token != ".Stmts":
            output.append(token)
    return output


submitted = [token for token in third_argument_of_funcdef(
    Path("/candidate/solution.mpy").read_text()
) if token != ".Stmts"]
claimed = expand(["targetBody"])
submitted_text = " ".join(submitted)
claimed_text = " ".join(claimed)
print("submitted_token_count", len(submitted))
print("expanded_claim_token_count", len(claimed))
print("submitted_sha256", hashlib.sha256(submitted_text.encode()).hexdigest())
print("expanded_claim_sha256", hashlib.sha256(claimed_text.encode()).hexdigest())
print("constructor_level_equal", submitted == claimed)
if submitted != claimed:
    for index, (left, right) in enumerate(zip(submitted, claimed)):
        if left != right:
            print("first_mismatch", index, left, right)
            break
assert submitted == claimed
