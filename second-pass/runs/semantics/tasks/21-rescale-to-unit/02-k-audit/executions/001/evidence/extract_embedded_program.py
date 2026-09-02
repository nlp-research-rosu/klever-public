#!/usr/bin/env python3
"""Extract the Module(...) term embedded in verification.k's #runRescale rule."""

from __future__ import annotations

from pathlib import Path

SOURCE = Path("/tmp/audit-work/21-rescale-to-unit/verification.k")
OUTPUT = Path("/tmp/audit-work/21-rescale-to-unit/extracted-embedded-program.mpy")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    marker = "#loadAll(Module("
    marker_at = text.index(marker)
    start = marker_at + len("#loadAll(")
    depth = 0
    in_string = False
    escaped = False
    end = None
    for index, character in enumerate(text[start:], start):
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
                end = index + 1
                break
    if end is None:
        raise RuntimeError("unbalanced embedded Module term")
    extracted = text[start:end]
    # K source accepts the internal empty-list token, while the external .mpy
    # scanner spells that same production as an empty constructor argument.
    extracted = extracted.replace("FreeVars(.ParamNames)", "FreeVars()")
    OUTPUT.write_text(extracted + "\n", encoding="utf-8")
    print(f"source={SOURCE}")
    print(f"output={OUTPUT}")
    print(f"start_offset={start} end_offset={end} bytes={len(extracted.encode())}")


if __name__ == "__main__":
    main()
