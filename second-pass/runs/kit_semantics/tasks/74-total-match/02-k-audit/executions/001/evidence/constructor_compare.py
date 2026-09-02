#!/usr/bin/env python3
"""Compare the submitted module with both entry-claim Module terms after K parsing."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/74-total-match")
DEFINITION = WORK / "audit-verification-kompiled"


def extract_balanced_module(text: str, start: int) -> tuple[str, int]:
    module_start = text.index("Module(", start)
    depth = 0
    in_string = False
    escaped = False
    for offset in range(module_start, len(text)):
        char = text[offset]
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
                return text[module_start : offset + 1] + "\n", offset + 1
    raise ValueError("unterminated Module term")


def parse_to_json(source: Path, destination: Path) -> object:
    command = [
        "kast",
        str(source),
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "--expand-macros",
        "--output",
        "json",
        "--output-file",
        str(destination),
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print("COMMAND:", " ".join(command))
    print(completed.stdout, end="")
    print("KAST_EXIT:", completed.returncode)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    return json.loads(destination.read_text())


def digest_json(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    spec_text = (WORK / "spec.k").read_text()
    cursor = 0
    extracted: list[Path] = []
    while True:
        load_start = spec_text.find("#loadAll(", cursor)
        if load_start < 0:
            break
        term, cursor = extract_balanced_module(spec_text, load_start)
        # The claim grammar spells the empty statement list as `.Stmts`;
        # py2mpy emits the same list constructor by leaving the list position
        # empty. The program parser accepts the latter spelling.
        empty_stmts = term.count(".Stmts")
        term = term.replace(".Stmts", "")
        path = WORK / f"extracted-entry-module-{len(extracted) + 1}.mpy"
        path.write_text(term)
        extracted.append(path)
        print(
            f"NORMALIZATION {path.name}: explicit_empty_stmts={empty_stmts} "
            "replacement=empty-list-position"
        )

    if len(extracted) != 2:
        raise AssertionError(f"expected two entry modules, found {len(extracted)}")

    sources = [WORK / "solution.mpy", *extracted]
    parsed = []
    for index, source in enumerate(sources):
        destination = WORK / f"parsed-module-{index}.json"
        term = parse_to_json(source, destination)
        parsed.append(term)
        print(f"PARSED_SHA256 {source.name}: {digest_json(term)}")

    for index, entry_term in enumerate(parsed[1:], start=1):
        equal = entry_term == parsed[0]
        print(f"ENTRY_{index}_CONSTRUCTOR_EQUAL={str(equal).lower()}")
        if not equal:
            raise AssertionError(f"entry {index} module differs from solution.mpy")

    print("CONSTRUCTOR_COMPARISON: PASS")


if __name__ == "__main__":
    main()
