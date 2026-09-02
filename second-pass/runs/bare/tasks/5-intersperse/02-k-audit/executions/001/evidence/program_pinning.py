#!/usr/bin/env python3
"""Mechanically compare the submitted program term with the term embedded in SPEC."""

from pathlib import Path


def balanced_module(text: str) -> str:
    start = text.index("Module(")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
                return text[start : index + 1]
    raise ValueError("unbalanced Module term")


def remove_layout(text: str) -> str:
    output = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    return "".join(output)


def main() -> None:
    solution_path = Path("/tmp/audit-work/reconstruction/solution.mpy")
    spec_path = Path("/tmp/audit-work/reconstruction/spec.k")
    solution_text = solution_path.read_text(encoding="utf-8")
    spec_text = spec_path.read_text(encoding="utf-8")

    submitted = remove_layout(balanced_module(solution_text))
    claimed = remove_layout(balanced_module(spec_text))
    same_surface = submitted == claimed
    print(f"submitted_program_normalized_chars={len(submitted)}")
    print(f"claimed_program_normalized_chars={len(claimed)}")
    print(f"program_surface_identical_ignoring_layout={same_surface}")
    if not same_surface:
        for index, (left, right) in enumerate(zip(submitted, claimed)):
            if left != right:
                print(f"first_surface_difference_offset={index}")
                print(f"submitted_context={submitted[max(0, index-30):index+60]!r}")
                print(f"claimed_context={claimed[max(0, index-30):index+60]!r}")
                break
        print("surface_note=SPEC spells the empty Stmts unit as .Stmts; parser-level comparison follows")


if __name__ == "__main__":
    main()
