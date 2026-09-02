#!/usr/bin/env python3
"""Split the submitted six-claim spec into independently runnable modules."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/reconstruction/spec.k")
OUTPUT_DIR = SOURCE.parent


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    starts: list[int] = []
    cursor = 0
    marker = "  claim\n"
    while True:
        index = text.find(marker, cursor)
        if index < 0:
            break
        starts.append(index)
        cursor = index + len(marker)

    if len(starts) != 6:
        raise RuntimeError(f"expected six claims, found {len(starts)}")

    for number, start in enumerate(starts, 1):
        next_claim = starts[number] if number < len(starts) else text.index("endmodule", start)
        between = text[start:next_claim]
        next_comment = between.find("\n  //")
        if next_comment >= 0:
            between = between[:next_comment]
        claim = between.rstrip()
        module_name = f"SPEC-CLAIM-{number}"
        output = OUTPUT_DIR / f"spec-claim-{number}.k"
        output.write_text(
            'requires "verification.k"\n\n'
            f"module {module_name}\n"
            "  imports VERIFICATION\n\n"
            f"{claim}\n"
            "endmodule\n",
            encoding="utf-8",
        )
        print(f"{number}: {output} module={module_name} bytes={output.stat().st_size}")


if __name__ == "__main__":
    main()
