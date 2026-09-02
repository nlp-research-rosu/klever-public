#!/usr/bin/env python3
"""Create a source-level inventory of every K declaration and rule block."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/tmp/audit-work/anti-shuffle-audit")
REFERENCE = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/09_rule_inventory.md")

paths = sorted(REFERENCE.rglob("*.k"))
paths += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(
    r"^(?:(requires|module|endmodule)\b|  "
    r"(imports|configuration|syntax|context|rule|claim|alias)\b)"
)
known_attrs = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "symbol",
    "macro",
    "macro-rec",
    "no-evaluators",
    "strict",
    "seqstrict",
    "hook",
    "cell",
    "assoc",
    "comm",
    "unit",
    "idem",
    "format",
    "token",
    "avoid",
)
bracket_re = re.compile(r"\[([^\]]*)\]")

global_kinds: Counter[str] = Counter()
global_attrs: Counter[str] = Counter()
rendered: list[str] = []
rendered.append("# Exhaustive K source declaration/rule inventory")
rendered.append("")
rendered.append(
    "The inventory is generated from the trusted scratch copy plus the candidate "
    "proof sources. Every declaration-start block is reproduced with source lines; "
    "file hashes and counts make omissions detectable."
)
rendered.append("")

for path in paths:
    data = path.read_bytes()
    lines = data.decode("utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))

    rel = path.relative_to(ROOT)
    sha = hashlib.sha256(data).hexdigest()
    local_kinds: Counter[str] = Counter(kind for _, kind in starts)
    global_kinds.update(local_kinds)

    rendered.append(f"## `{rel}`")
    rendered.append("")
    rendered.append(
        f"- SHA-256: `{sha}`; source lines: {len(lines)}; "
        f"declaration blocks: {len(starts)}"
    )
    rendered.append(
        "- Kinds: "
        + ", ".join(f"`{key}`={local_kinds[key]}" for key in sorted(local_kinds))
    )
    rendered.append("")

    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        # Exclude blank/comment-only tail before the next declaration.
        while end > start + 1:
            stripped = lines[end - 1].strip()
            if not stripped or stripped.startswith("//"):
                end -= 1
            else:
                break
        block = lines[start:end]
        attributes: list[str] = []
        for line in block:
            for group in bracket_re.findall(line):
                for normalized in known_attrs:
                    if re.search(rf"(?<![-\w]){re.escape(normalized)}(?![-\w])", group):
                        attributes.append(normalized)
                        global_attrs[normalized] += 1
        attr_text = ", ".join(attributes) if attributes else "none"
        rendered.append(
            f"### {kind} `{rel}:{start + 1}-{max(start + 1, end)}` "
            f"(attributes: {attr_text})"
        )
        rendered.append("")
        rendered.append("```k")
        for line_no, line in enumerate(block, start + 1):
            rendered.append(f"{line_no:04d}: {line}")
        rendered.append("```")
        rendered.append("")

rendered.insert(
    4,
    "Global declaration kinds: "
    + ", ".join(f"`{key}`={global_kinds[key]}" for key in sorted(global_kinds)),
)
rendered.insert(
    5,
    "Global source attributes: "
    + ", ".join(f"`{key}`={global_attrs[key]}" for key in sorted(global_attrs)),
)
OUTPUT.write_text("\n".join(rendered) + "\n", encoding="utf-8")
print(f"output={OUTPUT}")
print(f"files={len(paths)}")
print("kinds=" + json.dumps(dict(sorted(global_kinds.items())), sort_keys=True))
print("attributes=" + json.dumps(dict(sorted(global_attrs.items())), sort_keys=True))
