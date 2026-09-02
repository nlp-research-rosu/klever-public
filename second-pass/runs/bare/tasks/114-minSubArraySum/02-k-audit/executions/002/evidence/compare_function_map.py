#!/usr/bin/env python3
"""Compare solutionFunctions closures with FuncDef nodes in submitted solution.mpy."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

VERIFICATION = Path("/tmp/audit-work/source/verification.k")
SUBMITTED = Path("/candidate/solution.mpy")
DEFINITION = Path("/tmp/audit-work/build/verification-kompiled")


def parse(path: Path, module: str, sort: str) -> object:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        module,
        "--sort",
        sort,
        "--output",
        "json",
    ]
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )
    print(f"command={command!r}")
    print(f"exit_status={completed.returncode}")
    print(f"stderr={completed.stderr!r}")
    if completed.returncode:
        raise RuntimeError("kast failed")
    return json.loads(completed.stdout)["term"]


def balanced_terms(text: str, constructor: str) -> list[tuple[int, int, str]]:
    results: list[tuple[int, int, str]] = []
    position = 0
    marker = constructor + "("
    while True:
        start = text.find(marker, position)
        if start < 0:
            return results
        depth = 0
        in_string = False
        escaped = False
        for index in range(start + len(constructor), len(text)):
            character = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
                continue
            if character == '"':
                in_string = True
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    results.append((start, index + 1, text[start : index + 1]))
                    position = index + 1
                    break
        else:
            raise ValueError(f"unbalanced {constructor}")


def split_top_level_arguments(term: str) -> list[str]:
    opening = term.index("(")
    body = term[opening + 1 : -1]
    parts: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, character in enumerate(body):
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            parts.append(body[start:index].strip())
            start = index + 1
    parts.append(body[start:].strip())
    return parts


def main() -> int:
    text = VERIFICATION.read_text(encoding="utf-8")
    marker = "rule solutionFunctions =>"
    start = text.index(marker) + len(marker)
    end = text.index("syntax Program", start)
    rhs = text[start:end].strip().replace(".Stmts", "")
    print(f"normalized_empty_Stmts_markers={text[start:end].count('.Stmts')}")

    definitions: dict[str, str] = {}
    for _start, _end, function_def in balanced_terms(
        SUBMITTED.read_text(encoding="utf-8"), "FuncDef"
    ):
        arguments = split_top_level_arguments(function_def)
        if len(arguments) != 3:
            raise ValueError("unexpected FuncDef arity")
        name, params, body = arguments
        definitions[name] = f"closure({params}, {body})"

    mapped: dict[str, str] = {}
    for closure_start, _closure_end, closure in balanced_terms(rhs, "closure"):
        prefix = rhs[:closure_start]
        map_arrow = prefix.rfind("|->")
        quote_end = prefix.rfind('"', 0, map_arrow)
        quote_start = prefix.rfind('"', 0, quote_end)
        name = prefix[quote_start : quote_end + 1]
        mapped[name] = closure

    print(f"function_def_count={len(definitions)}")
    print(f"map_closure_count={len(mapped)}")
    print("definition_names=" + json.dumps(sorted(definitions)))
    print("mapped_names=" + json.dumps(sorted(mapped)))
    names_equal = set(definitions) == set(mapped)
    bodies_equal = names_equal
    for index, name in enumerate(sorted(definitions), 1):
        expected_path = Path(f"/tmp/audit-work/source/expected-closure-{index}.kterm")
        mapped_path = Path(f"/tmp/audit-work/source/mapped-closure-{index}.kterm")
        expected_path.write_text(definitions[name] + "\n", encoding="utf-8")
        mapped_path.write_text(mapped[name] + "\n", encoding="utf-8")
        expected = parse(expected_path, "VERIFICATION", "Function")
        actual = parse(mapped_path, "VERIFICATION", "Function")
        equal = expected == actual
        print(f"closure_equal:{name}={equal}")
        bodies_equal = bodies_equal and equal
    print(f"function_names_equal={names_equal}")
    print(f"params_and_bodies_equal={bodies_equal}")
    return 0 if len(definitions) == 2 and names_equal and bodies_equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
