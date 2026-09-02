#!/usr/bin/env python3
"""Create a deterministic inventory of local K declarations."""

import argparse
import re
from pathlib import Path


START = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|context|"
    r"rule|claim|alias)\b"
)
DECL = re.compile(r"^\s*(configuration|syntax|context|rule|claim|alias)\b")
ATTR = re.compile(
    r"\b(function|total|functional|simplification|priority|concrete|"
    r"anywhere|macro-rec|macro|token|owise|no-evaluators|symbol)\b"
)


def compact(lines):
    return " ".join(
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("//")
    )[:5000]


def declarations(path: Path):
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for pos, start in enumerate(starts):
        match = DECL.match(lines[start])
        if not match:
            continue
        stop = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        body = lines[start:stop]
        code_body = [
            line for line in body if not line.lstrip().startswith("//")
        ]
        attrs = sorted(set(ATTR.findall("\n".join(code_body))))
        yield start + 1, stop, match.group(1), ",".join(attrs) or "-", compact(body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--extra", type=Path, action="append", default=[])
    args = parser.parse_args()

    paths = sorted(args.root.rglob("*.k")) + args.extra
    print("file\tstart\tend\tkind\tattributes\tdeclaration")
    total = 0
    counts = {}
    for path in paths:
        display = str(path)
        for start, stop, kind, attrs, body in declarations(path):
            total += 1
            counts[kind] = counts.get(kind, 0) + 1
            safe_body = body.replace("\t", " ")
            print(f"{display}\t{start}\t{stop}\t{kind}\t{attrs}\t{safe_body}")
    summary = ",".join(f"{key}={counts[key]}" for key in sorted(counts))
    print(f"# total={total} {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
