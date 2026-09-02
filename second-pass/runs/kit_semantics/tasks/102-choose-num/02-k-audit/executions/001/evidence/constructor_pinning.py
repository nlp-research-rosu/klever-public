#!/usr/bin/env python3
"""Mechanically compare translated constructors with all claim-embedded bodies."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


WORK = Path("/tmp/audit-work/102-choose-num")


def balanced_call(text: str, start: int) -> tuple[str, int]:
    open_paren = text.find("(", start)
    assert open_paren >= 0
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1], index + 1
    raise AssertionError(f"unbalanced call at offset {start}")


def calls_named(text: str, name: str) -> list[str]:
    found: list[str] = []
    offset = 0
    marker = name + "("
    while True:
        start = text.find(marker, offset)
        if start < 0:
            return found
        call, offset = balanced_call(text, start)
        found.append(call)


def split_args(call: str) -> list[str]:
    open_paren = call.find("(")
    body = call[open_paren + 1 : -1]
    args: list[str] = []
    depth = 0
    in_string = False
    escaped = False
    start = 0
    for index, char in enumerate(body):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(body[start:index].strip())
            start = index + 1
    args.append(body[start:].strip())
    return args


def kast_term(source: str, filename: str) -> dict:
    # `.Stmts` is K's internal empty-list constructor. The external MPY
    # concrete grammar renders the same list unit as the empty string.
    concrete_source = source.replace(".Stmts", "")
    with tempfile.TemporaryDirectory(prefix="pinning-", dir=WORK) as temp_name:
        path = Path(temp_name) / filename
        path.write_text(concrete_source + "\n")
        command = [
            "kast",
            str(path),
            "--definition",
            str(WORK / "audit-runtime-kompiled"),
            "--output",
            "json",
        ]
        print("COMMAND:", " ".join(command))
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        print(f"EXIT_STATUS: {result.returncode}")
        if result.stderr:
            print(result.stderr.rstrip())
        assert result.returncode == 0
        return json.loads(result.stdout)["term"]


def digest(term: dict) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    translated_source = (WORK / "solution.mpy").read_text()
    spec_source = (WORK / "spec.k").read_text()

    translated_term = kast_term(translated_source, "translated.mpy")
    translated_hash = digest(translated_term)
    print(f"translated_constructor_sha256={translated_hash}")

    load_marker = spec_source.index("#loadAll(")
    module_start = spec_source.index("Module(", load_marker)
    claim_module, _ = balanced_call(spec_source, module_start)
    claim_module_term = kast_term(claim_module, "load-claim-module.mpy")
    print(f"load_claim_constructor_sha256={digest(claim_module_term)}")
    assert claim_module_term == translated_term

    closure_calls = calls_named(spec_source, "closureVal")
    assert len(closure_calls) == 2, len(closure_calls)
    for index, closure in enumerate(closure_calls, 1):
        args = split_args(closure)
        assert len(args) == 5, (index, args)
        assert args[0] == '"x"' and args[1] == '"y"'
        assert args[2] == ".ParamNames" and args[4] == "0"
        wrapped = f'Module(FuncDef("choose_num", Params("x", "y"), {args[3]}))'
        closure_term = kast_term(wrapped, f"closure-{index}.mpy")
        closure_hash = digest(closure_term)
        print(f"closure_{index}_constructor_sha256={closure_hash}")
        assert closure_term == translated_term

    print("CONSTRUCTOR_PINNING=PASS")


if __name__ == "__main__":
    main()
