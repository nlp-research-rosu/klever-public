#!/usr/bin/env python3
"""Produce a complete sentence-level inventory of the K sources under audit."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/fresh")
SEMANTICS = ROOT / "reference-semantics"
FILES = [
    SEMANTICS / "semantics.k",
    *sorted((SEMANTICS / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^(?P<indent> *)(?P<kind>requires|module|endmodule|imports|configuration|"
    r"syntax|context|rule|claim|alias)\b"
)
ATTRIBUTE = re.compile(r"\[([^\]]+)\]")


def sentences(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if not match or len(match.group("indent")) > 2:
            continue
        starts.append((index, match.group("kind")))
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:stop]).rstrip()
        yield start + 1, stop, kind, text


def classify(path: Path, kind: str, text: str, ordinal: int) -> tuple[str, str]:
    if path.name == "verification.k":
        if kind == "rule":
            if ordinal == 1:
                return (
                    "ACCEPT_MACRO_PENDING_PIN_CHECK",
                    "macro definition of submitted function body",
                )
            if ordinal in {2, 3, 4}:
                return (
                    "ACCEPT_MATHEMATICAL_DEFINITION",
                    "guard-complete recursive equations for overlapCount",
                )
            if ordinal in {5, 6, 7, 8, 9}:
                return (
                    "ACCEPT_INTERNAL_PROOF_MACHINE",
                    "rules operate only on fresh #overlapEval/#overlapAcc items",
                )
            if ordinal == 10:
                return (
                    "REJECT_OPERATIONAL_BRIDGE",
                    "preempts fixed closure execution without connection theorem",
                )
        return (
            "DECLARATION_OR_IMPORT",
            "proof-local declaration; assessed with its defining rules",
        )
    if path.name == "spec.k":
        if kind == "claim":
            return ("TARGET_CLAIM", "positive proof obligation")
        return ("DECLARATION_OR_IMPORT", "specification structure")
    return (
        "ACCEPT_SELECTED_FIXED_SEMANTICS",
        "launcher-verified supplied semantics; task-used subset reviewed in detail",
    )


def one_line(text: str) -> str:
    return " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("//")
    )


def without_comments(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def main() -> int:
    print(
        "file\tstart\tend\tkind\tattributes\tflags\tdecision\treason\tsentence"
    )
    counts: dict[str, int] = {}
    verification_rule_ordinal = 0
    total = 0
    for path in FILES:
        relative = path.relative_to(ROOT).as_posix()
        for start, stop, kind, text in sentences(path):
            total += 1
            counts[kind] = counts.get(kind, 0) + 1
            if path.name == "verification.k" and kind == "rule":
                verification_rule_ordinal += 1
                ordinal = verification_rule_ordinal
            else:
                ordinal = 0
            code = without_comments(text)
            attrs = ";".join(ATTRIBUTE.findall(code))
            flags = []
            lowered = code.lower()
            for flag in (
                "function",
                "total",
                "functional",
                "macro",
                "macro-rec",
                "simplification",
                "concrete",
                "priority",
                "owise",
                "symbol",
                "no-evaluators",
                "strict",
                "seqstrict",
            ):
                if re.search(rf"\b{re.escape(flag)}\b", lowered):
                    flags.append(flag)
            decision, reason = classify(path, kind, text, ordinal)
            sentence = one_line(text).replace("\t", " ")
            print(
                f"{relative}\t{start}\t{stop}\t{kind}\t{attrs}\t"
                f"{','.join(flags)}\t{decision}\t{reason}\t{sentence}"
            )
    print(f"# total={total}")
    print(f"# counts={dict(sorted(counts.items()))}")
    print(f"# verification_rule_count={verification_rule_ordinal}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
