#!/usr/bin/env python3
"""Mechanical source-to-entry-term comparison and concrete adequacy witnesses."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path


FRESH = Path("/tmp/audit-work/fresh")
DEFINITION = FRESH / "audit-runtime-kompiled"


def balanced_call(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
                return text[start : index + 1]
    raise AssertionError("unbalanced constructor call")


def load_add(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add


def mathematical_summary(values: list[int]) -> int:
    return sum(value for index, value in enumerate(values)
               if index % 2 == 1 and value % 2 == 0)


def main() -> None:
    spec_text = (FRESH / "spec.k").read_text(encoding="utf-8")
    entry_start = spec_text.index("claim [add-entry]:")
    function_start = spec_text.index("FuncDef(", entry_start)
    function_term = balanced_call(spec_text, function_start)
    # `.Stmts` is the explicit sequence identity accepted in rule syntax.
    # Program syntax uses the corresponding empty position; removing only
    # these identities is the declared semantically inert normalization.
    function_term = function_term.replace(".Stmts", "")
    extracted = FRESH / "entry-function-extracted.mpy"
    extracted.write_text(f"Module({function_term})\n", encoding="utf-8")

    commands = [
        [
            "kast",
            "solution.regenerated.mpy",
            "--definition",
            str(DEFINITION),
            "--output",
            "json",
        ],
        [
            "kast",
            extracted.name,
            "--definition",
            str(DEFINITION),
            "--output",
            "json",
        ],
    ]
    parsed_terms = []
    for command in commands:
        print("COMMAND:", " ".join(command))
        result = subprocess.run(
            command,
            cwd=FRESH,
            check=False,
            capture_output=True,
            text=True,
        )
        print("EXIT:", result.returncode)
        if result.stderr:
            print(result.stderr, end="")
        assert result.returncode == 0
        parsed_terms.append(json.loads(result.stdout)["term"])

    assert parsed_terms[0] == parsed_terms[1]
    print(
        "CONSTRUCTOR_IDENTITY=PASS "
        "translated solution Module(FuncDef(...)) equals entry-claim FuncDef"
    )

    canonical = load_add(Path("/reference/canonical.py"), "canonical_stage4")
    generated = load_add(FRESH / "solution.py", "generated_stage4")
    witnesses = [
        [4, 2, 6, 7],
        [1, -2, 3, -4],
        [10],
        [9, 0],
    ]
    for values in witnesses:
        summary = mathematical_summary(values)
        canonical_value = canonical(list(values))
        generated_value = generated(list(values))
        assert summary == canonical_value == generated_value
        print(
            f"WITNESS values={values!r} nonempty={bool(values)} "
            f"allInts={all(type(value) is int for value in values)} "
            f"addSummary={summary} canonical={canonical_value} "
            f"generated={generated_value}"
        )


if __name__ == "__main__":
    main()
