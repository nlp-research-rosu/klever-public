"""Create a line-numbered inventory of K declarations and rules under review."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^(?:requires\b|\s*(?:module|endmodule|imports|syntax|configuration|"
    r"context(?:\s+alias)?|rule|claim)\b)"
)
KIND = re.compile(
    r"^(?P<dependency>requires)\b|^\s*(?P<declaration>module|endmodule|imports|"
    r"syntax|configuration|context(?:\s+alias)?|rule|claim)\b"
)


def blocks(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) and not line.lstrip().startswith("//")
    ]
    result: list[tuple[int, str, str]] = []
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:stop]).rstrip()
        kind_match = KIND.match(lines[start])
        assert kind_match is not None
        kind = kind_match.group("dependency") or kind_match.group("declaration")
        assert kind is not None
        result.append((start + 1, kind, text))
    return result


def main() -> None:
    total: Counter[str] = Counter()
    for path in FILES:
        relative = path.relative_to(ROOT)
        entries = blocks(path)
        local = Counter(kind for _, kind, _ in entries)
        total.update(local)
        print(f"FILE {relative} blocks={len(entries)} kinds={dict(local)}")
        for ordinal, (line, kind, text) in enumerate(entries, 1):
            flags = [
                flag
                for flag in (
                    "function",
                    "total",
                    "functional",
                    "symbol",
                    "no-evaluators",
                    "priority",
                    "simplification",
                    "concrete",
                    "owise",
                    "strict",
                    "seqstrict",
                    "macro",
                )
                if re.search(rf"\b{re.escape(flag)}\b", text)
            ]
            print(
                f"ENTRY {relative}:{line} ordinal={ordinal} "
                f"kind={kind} flags={','.join(flags) or '-'}"
            )
            print(text)
            print("END_ENTRY")
    print("TOTAL_KINDS", dict(total))


if __name__ == "__main__":
    main()
