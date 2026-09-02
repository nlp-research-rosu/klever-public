#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and spec closures."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def balanced_call_contents(text: str, marker: str):
    start = 0
    while True:
        marker_at = text.find(marker, start)
        if marker_at < 0:
            return
        open_at = marker_at + len(marker) - 1
        depth = 0
        in_string = False
        escaped = False
        for index in range(open_at, len(text)):
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
                    yield marker_at, index + 1, text[open_at + 1 : index]
                    start = index + 1
                    break
        else:
            raise RuntimeError(f"unterminated {marker} occurrence at {marker_at}")


def split_top_level_arguments(contents: str) -> list[str]:
    result: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(contents):
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
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            result.append(contents[start:index].strip())
            start = index + 1
    result.append(contents[start:].strip())
    return result


def kast(path: Path, definition: Path) -> dict:
    command = [
        "kast",
        str(path),
        "--definition",
        str(definition),
        "--input",
        "program",
        "--output",
        "json",
    ]
    process = subprocess.run(command, check=False, text=True, capture_output=True)
    if process.returncode != 0:
        raise RuntimeError(
            f"kast failed ({process.returncode}) for {path}: {process.stderr}"
        )
    return json.loads(process.stdout)


def kast_rule_term(term_text: str, definition: Path) -> dict:
    expression = f"<k> {term_text} => {term_text} </k>"
    command = [
        "kast",
        "--definition",
        str(definition),
        "--input",
        "rule",
        "--output",
        "json",
        "--expression",
        expression,
    ]
    process = subprocess.run(command, check=False, text=True, capture_output=True)
    if process.returncode != 0:
        raise RuntimeError(
            f"kast rule parse failed ({process.returncode}): {process.stderr}"
        )
    parsed = json.loads(process.stdout)
    try:
        return parsed["term"]["args"][0]["lhs"]
    except (KeyError, IndexError, TypeError) as err:
        raise RuntimeError("unexpected kast rule JSON shape") from err


def collect_labels(node, labels: set[str]) -> None:
    if isinstance(node, dict):
        if node.get("node") == "KApply":
            label = node.get("label")
            if isinstance(label, dict) and isinstance(label.get("name"), str):
                labels.add(label["name"])
        for value in node.values():
            collect_labels(value, labels)
    elif isinstance(node, list):
        for value in node:
            collect_labels(value, labels)


def digest_json(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: program_pinning.py SOLUTION.mpy SPEC.k DEFINITION TMPDIR",
            file=sys.stderr,
        )
        return 2
    solution_path = Path(sys.argv[1])
    spec_path = Path(sys.argv[2])
    definition = Path(sys.argv[3])
    tmpdir = Path(sys.argv[4])
    tmpdir.mkdir(parents=True, exist_ok=True)

    trusted_program_term = kast(solution_path, definition)
    trusted_term = trusted_program_term["term"]
    trusted_hash = digest_json(trusted_term)
    labels: set[str] = set()
    collect_labels(trusted_term, labels)
    print(f"solution_kast_sha256={trusted_hash}")
    print(f"solution_constructor_labels={len(labels)}")
    for label in sorted(labels):
        print(f"  {label}")

    spec_text = spec_path.read_text()
    closures = list(balanced_call_contents(spec_text, "closureVal("))
    print(f"spec_closure_occurrences={len(closures)}")
    all_equal = True
    for number, (_start, _end, contents) in enumerate(closures, 1):
        arguments = split_top_level_arguments(contents)
        if len(arguments) != 4:
            raise RuntimeError(
                f"closure {number} has {len(arguments)} top-level arguments"
            )
        name, trailing_parameters, body, defining_env = arguments
        header_ok = (
            " ".join(name.split()) == '"arr"'
            and " ".join(trailing_parameters.split()) == ".ParamNames"
            and " ".join(defining_env.split()) == "0"
        )
        wrapped = (
            "Module(\n"
            '  FuncDef("count_nums", Params("arr"),\n'
            f"{body}\n"
            "  ))\n"
        )
        extracted_path = tmpdir / f"closure-{number}.mpy"
        extracted_path.write_text(wrapped)
        extracted_term = kast_rule_term(wrapped, definition)
        extracted_hash = digest_json(extracted_term)
        equal = extracted_term == trusted_term
        all_equal &= header_ok and equal
        print(
            f"closure_{number}: header_ok={header_ok} kast_equal={equal} "
            f"kast_sha256={extracted_hash} source={extracted_path}"
        )

    print(f"PROGRAM_PINNING={'PASS' if all_equal and closures else 'FAIL'}")
    return 0 if all_equal and closures else 1


if __name__ == "__main__":
    sys.exit(main())
