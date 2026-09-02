#!/usr/bin/env python3
"""Mechanically compare the regenerated constructor term with the entry claim."""

from __future__ import annotations

from pathlib import Path


def balanced_term(text: str, start: int) -> str:
    opening = text.find("(", start)
    if opening < 0:
        raise ValueError("opening parenthesis not found")
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
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
    raise ValueError("unbalanced term")


def strip_layout(text: str) -> str:
    output: list[str] = []
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
            output.append(character)
        elif not character.isspace():
            output.append(character)
    return "".join(output)


def main() -> None:
    generated = Path(
        "/tmp/audit-work/reconstruction/solution.regenerated.mpy"
    ).read_text()
    spec = Path("/tmp/audit-work/reconstruction/spec.k").read_text()
    entry_start = spec.index("claim [correct-bracketing]:")
    load_start = spec.index("Module(", entry_start)
    embedded = balanced_term(spec, load_start)
    Path(
        "/tmp/audit-work/reconstruction/entry-embedded.mpy"
    ).write_text(embedded + "\n")
    generated_internal = generated.replace(
        "Return(Bool(false)),\n        ))",
        "Return(Bool(false)),\n        .Stmts))",
    )
    Path(
        "/tmp/audit-work/reconstruction/generated-identity-rule.k"
    ).write_text(
        f"<k> #loadAll({generated_internal.strip()}) => .K </k>\n"
    )
    Path(
        "/tmp/audit-work/reconstruction/embedded-identity-rule.k"
    ).write_text(f"<k> #loadAll({embedded.strip()}) => .K </k>\n")
    generated_normalized = strip_layout(generated)
    embedded_normalized = strip_layout(embedded)
    unit_normalized = embedded_normalized.replace(",.Stmts))", ",))", 1)
    print(f"generated_term_length={len(generated_normalized)}")
    print(f"embedded_term_length={len(embedded_normalized)}")
    print(
        "constructor_term_exact_after_layout_normalization="
        f"{generated_normalized == embedded_normalized}"
    )
    print(
        "constructor_term_equal_after_empty_stmts_unit_normalization="
        f"{generated_normalized == unit_normalized}"
    )
    normalized_entry = strip_layout(spec[entry_start:])
    expected_call = 'Call(Name("correct_bracketing"),str(S:IntSeq))'
    print(
        "entry_calls_bound_name_with_symbolic_string="
        f"{expected_call in normalized_entry}"
    )
    if generated_normalized != unit_normalized:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
