#!/usr/bin/env python3
"""Split the six wrong-interpretation witness claims for isolated execution."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/unsound-witness/unsound-interpretation-spec.k")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    marker = "  claim\n"
    starts: list[int] = []
    cursor = 0
    while True:
        index = text.find(marker, cursor)
        if index < 0:
            break
        starts.append(index)
        cursor = index + len(marker)
    if len(starts) != 6:
        raise RuntimeError(f"expected six claims, got {len(starts)}")
    for number, start in enumerate(starts, 1):
        end = starts[number] if number < len(starts) else text.index("endmodule", start)
        claim = text[start:end].rstrip()
        module = f"UNSOUND-WITNESS-{number}"
        output = SOURCE.parent / f"unsound-witness-{number}.k"
        output.write_text(
            'requires "unsound-interpretation.k"\n\n'
            f"module {module}\n"
            "  imports UNSOUND-INTERPRETATION\n\n"
            f"{claim}\n"
            "endmodule\n",
            encoding="utf-8",
        )
        print(f"{number}: {output} module={module}")


if __name__ == "__main__":
    main()
