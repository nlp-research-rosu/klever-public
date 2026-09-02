#!/usr/bin/env python3
"""Create mechanical ground instances and a body-sensitivity mutation."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("/tmp/audit-work/43-pairs-sum-to-zero")
SOURCE = ROOT / "candidate/spec.k"


def ground(module: str, input_term: str, expected: str) -> str:
    text = SOURCE.read_text()
    text = text.replace(
        'requires "verification.k"',
        'requires "candidate/verification.k"',
        1,
    )
    text = text.replace("module SPEC", f"module {module}", 1)
    text = text.replace("L:ISeq", input_term, 1)
    text = text.replace(
        "pyBool(hasZeroPair(L))",
        f"pyBool({expected})",
        1,
    )
    return text


def main() -> None:
    cases = [
        ("SPEC-GROUND-EMPTY", ".ISeq", "false", "04-ground-empty.k"),
        ("SPEC-GROUND-TWO-ZEROES", "0 :: 0 :: .ISeq", "true", "04-ground-two-zeroes.k"),
        ("SPEC-GROUND-NO-PAIR", "1 :: 2 :: .ISeq", "false", "04-ground-no-pair.k"),
    ]
    for module, input_term, expected, name in cases:
        path = ROOT / name
        path.write_text(ground(module, input_term, expected))
        print(f"wrote {path} input={input_term} expected={expected}")

    body = SOURCE.read_text()
    body = body.replace(
        'requires "verification.k"',
        'requires "candidate/verification.k"',
        1,
    )
    body = body.replace("module SPEC", "module SPEC-BODY-MUTATION", 1)
    replacements = body.count("Return(Bool(false))")
    assert replacements == 2
    body = body.replace("Return(Bool(false))", "Return(Bool(true))")
    path = ROOT / "04-body-mutation.k"
    path.write_text(body)
    print(
        f"wrote {path} replacements={replacements}; both executed and "
        "<program>-cell copies changed"
    )


if __name__ == "__main__":
    main()
