#!/usr/bin/env python3
"""Build an exhaustive lexical inventory of K declarations, rules, and claims.

This is intentionally lexical: each outer K sentence is preserved verbatim
(normalized to one display line), with source bounds and attributes.  It does
not treat the supplied semantics as an instruction or trust candidate prose.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k"))
FILES.extend([ROOT / "verification.k", ROOT / "spec.k"])

START = re.compile(
    r"^(?P<indent>[ \t]*)(?P<kind>syntax|rule|context|configuration|claim|alias)\b"
)
ENDMODULE = re.compile(r"^[ \t]*endmodule\b")
ATTR = re.compile(r"\[([^\[\]]+)\]")
KNOWN_ATTR = re.compile(
    r"^(?:"
    r"function|functional|total|no-evaluators|owise|concrete|"
    r"macro|macro-rec|strict(?:\([^)]*\))?|seqstrict(?:\([^)]*\))?|"
    r"priority\([^)]*\)|symbol(?:\([^)]*\))?|"
    r"assoc|comm|idem|unit\([^)]*\)|hook\([^)]*\)|"
    r"left|right|non-assoc|token|bracket|avoid|prefer|"
    r"simplification|trusted|anywhere|heat|cool"
    r")$"
)

# Outer-sentence start lines whose behavior is actually reachable from the
# submitted #chooseNum closure (or from loading the same module in the
# reviewer-authored concrete harness).  The inventory keeps all other fixed
# rules too and explicitly marks them unreachable for this theorem.
RELEVANT_STARTS: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "reference-semantics/semantics/core.k": {
        25,
        36,
        37,
        38,
        39,
        41,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        195,
        199,
        200,
        202,
        208,
        209,
        210,
    },
    "reference-semantics/semantics/operators.k": {10, 12, 15, 16, 17},
    "reference-semantics/semantics/int.k": {7, 13, 15, 19, 20, 25, 26},
    "reference-semantics/semantics/controls.k": {51, 52, 53, 54},
    "reference-semantics/semantics/functions.k": {
        8,
        14,
        63,
        64,
        78,
        80,
        85,
    },
    "reference-semantics/semantics/call.k": {19, 20, 21, 69},
    "verification.k": {8, 12, 13, 19},
    "spec.k": {11, 27, 45, 63, 81},
}


def mask_comments(text: str) -> str:
    """Mask // and nested /* */ comments, preserving offsets and newlines."""
    out = list(text)
    i = 0
    state = "code"
    depth = 0
    while i < len(text):
        c = text[i]
        n = text[i + 1] if i + 1 < len(text) else ""
        if state == "line":
            if c in "\r\n":
                state = "code"
            else:
                out[i] = " "
            i += 1
            continue
        if state == "block":
            if c == "/" and n == "*":
                out[i] = out[i + 1] = " "
                depth += 1
                i += 2
            elif c == "*" and n == "/":
                out[i] = out[i + 1] = " "
                depth -= 1
                i += 2
                if depth == 0:
                    state = "code"
            else:
                if c not in "\r\n":
                    out[i] = " "
                i += 1
            continue
        if state == "string":
            if c == "\\" and n:
                i += 2
            else:
                if c == '"':
                    state = "code"
                i += 1
            continue
        if c == "/" and n == "/":
            out[i] = out[i + 1] = " "
            state = "line"
            i += 2
        elif c == "/" and n == "*":
            out[i] = out[i + 1] = " "
            state = "block"
            depth = 1
            i += 2
        else:
            if c == '"':
                state = "string"
            i += 1
    return "".join(out)


def source_key(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sentences(path: Path):
    text = path.read_text()
    masked = mask_comments(text)
    lines = text.splitlines()
    masked_lines = masked.splitlines()
    starts: list[tuple[int, str]] = []
    module_ends: set[int] = set()
    for number, line in enumerate(masked_lines, 1):
        found = START.match(line)
        if found:
            starts.append((number, found.group("kind")))
        if ENDMODULE.match(line):
            module_ends.add(number)
    for index, (start, kind) in enumerate(starts):
        candidates = [len(lines) + 1]
        if index + 1 < len(starts):
            candidates.append(starts[index + 1][0])
        candidates.extend(line for line in module_ends if line > start)
        end_exclusive = min(candidates)
        end = end_exclusive - 1
        while end >= start and not masked_lines[end - 1].strip():
            end -= 1
        raw = "\n".join(lines[start - 1 : end])
        masked_raw = mask_comments(raw)
        normalized = " ".join(masked_raw.split())
        attributes = []
        for match in ATTR.finditer(masked_raw):
            for part in match.group(1).split(","):
                token = part.strip()
                if token and KNOWN_ATTR.fullmatch(token):
                    attributes.append(token)
        yield {
            "file": source_key(path),
            "start": start,
            "end": end,
            "kind": kind,
            "text": normalized,
            "attributes": attributes,
            "sha256": hashlib.sha256(normalized.encode()).hexdigest(),
        }


def disposition(entry: dict[str, object]) -> tuple[str, str]:
    file = str(entry["file"])
    start = int(entry["start"])
    kind = str(entry["kind"])
    if file == "verification.k":
        if start == 8:
            return (
                "LOCAL_INVOCATION_SYNTAX",
                "Accepted: proof-only constructor with no equation except the exact expansion at line 19.",
            )
        if start == 12:
            return (
                "LOCAL_DEFINITIONAL_SUMMARY",
                "Accepted: total mathematical function; its single rule covers all Int pairs.",
            )
        if start == 13:
            return (
                "LOCAL_DEFINITIONAL_SUMMARY",
                "Accepted: computes Y-pyMod(Y,2) and returns it iff it is >= X; no execution is replaced.",
            )
        if start == 19:
            return (
                "LOCAL_OPERATIONAL_BRIDGE",
                "Accepted subject to the separately recorded constructor/body, state-footprint, and sensitivity checks.",
            )
    if file == "spec.k":
        return (
            "TARGET_CLAIM",
            "Result-constraining reachability target; precondition satisfiability and closure checked separately.",
        )
    if start in RELEVANT_STARTS.get(file, set()):
        return (
            "FIXED_RELEVANT",
            "Accepted for this theorem after control/data-flow review against the executed Int/If/function-call fragment.",
        )
    if kind == "syntax" and "no-evaluators" in entry["attributes"]:
        return (
            "FIXED_UNUSED_OPAQUE",
            "Not reachable from the submitted program term; cannot influence its result, state, control, or claims.",
        )
    return (
        "FIXED_UNUSED",
        "Not reachable from the submitted program term; no task-answer rule or dependency from a target claim.",
    )


entries = []
for file in FILES:
    entries.extend(sentences(file))

counts = Counter(entry["kind"] for entry in entries)
dispositions = Counter()
for entry in entries:
    entry["disposition"], entry["assessment"] = disposition(entry)
    dispositions[entry["disposition"]] += 1

print("# Exhaustive K source inventory")
print()
print(f"Files: {len(FILES)}")
print(f"Sentences: {len(entries)}")
print("Kinds: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))
print(
    "Dispositions: "
    + ", ".join(f"{key}={dispositions[key]}" for key in sorted(dispositions))
)
print(
    "Simplification rules: "
    + str(
        sum(
            1
            for entry in entries
            if entry["kind"] == "rule"
            and "simplification" in entry["attributes"]
        )
    )
)
print(
    "Function declarations: "
    + str(
        sum(
            1
            for entry in entries
            if entry["kind"] == "syntax"
            and "function" in entry["attributes"]
        )
    )
)
print(
    "Functional declarations: "
    + str(
        sum(
            1
            for entry in entries
            if entry["kind"] == "syntax"
            and "functional" in entry["attributes"]
        )
    )
)
print(
    "Macro declarations: "
    + str(
        sum(
            1
            for entry in entries
            if entry["kind"] == "syntax"
            and any(attr in {"macro", "macro-rec"} for attr in entry["attributes"])
        )
    )
)
print(
    "Total declarations: "
    + str(
        sum(
            1
            for entry in entries
            if entry["kind"] == "syntax"
            and "total" in entry["attributes"]
        )
    )
)
print(
    "Opaque/no-evaluators declarations: "
    + str(
        sum(
            1
            for entry in entries
            if entry["kind"] == "syntax"
            and "no-evaluators" in entry["attributes"]
        )
    )
)
print(
    "Priority rules: "
    + str(
        sum(
            1
            for entry in entries
            if entry["kind"] == "rule"
            and any(attr.startswith("priority(") for attr in entry["attributes"])
        )
    )
)
print()

for number, entry in enumerate(entries, 1):
    attrs = ", ".join(entry["attributes"]) or "none"
    print(
        f"## K-{number:04d} — {entry['file']}:{entry['start']}"
        + (f"-{entry['end']}" if entry["end"] != entry["start"] else "")
    )
    print()
    print(f"- Kind: {entry['kind']}")
    print(f"- Attributes: {attrs}")
    print(f"- Normalized SHA-256: `{entry['sha256']}`")
    print(f"- Disposition: {entry['disposition']}")
    print(f"- Assessment: {entry['assessment']}")
    print(f"- Sentence: `{entry['text'].replace('`', chr(92) + '`')}`")
    print()
