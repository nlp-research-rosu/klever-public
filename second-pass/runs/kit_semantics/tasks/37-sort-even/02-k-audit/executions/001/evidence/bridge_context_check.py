#!/usr/bin/env python3
"""Check bridge-free dependency isolation and exact bridge/theorem context identity."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/37-sort-even")


def normalize(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("//") or not stripped:
            continue
        lines.append(stripped)
    return "".join(lines).replace(" ", "").replace("\t", "")


def operational_region(text: str, anchor: str) -> str:
    anchor_index = text.index(anchor)
    start = text.index("<k>", anchor_index)
    guard = "requires I >=Int 0"
    end = text.index(guard, start) + len(guard)
    return text[start:end]


def module_body(text: str, module_name: str) -> str:
    match = re.search(
        rf"(?ms)^module {re.escape(module_name)}\s*$"
        rf"(?P<body>.*?)^endmodule\s*$",
        text,
    )
    if not match:
        raise AssertionError(f"cannot find module {module_name}")
    return match.group("body")


def main() -> None:
    verification = (ROOT / "verification.k").read_text()
    connection = (ROOT / "spec-connection.k").read_text()

    no_bridge_body = module_body(verification, "VERIFICATION-NO-BRIDGE")
    bridge_body = module_body(verification, "VERIFICATION")
    assert "imports VERIFICATION-BASE" in no_bridge_body
    assert not re.search(r"(?m)^\s*imports VERIFICATION\s*$", no_bridge_body)
    assert "#loop(" not in no_bridge_body
    assert "imports VERIFICATION-BASE" in bridge_body
    assert "priority(40)" in bridge_body

    connection_module = module_body(connection, "SPEC-CONNECTION")
    assert "imports VERIFICATION-NO-BRIDGE" in connection_module
    assert not re.search(r"(?m)^\s*imports VERIFICATION\s*$", connection_module)

    bridge_region = operational_region(verification, "module VERIFICATION\n")
    theorem_region = operational_region(connection, "claim [loop-connection]:")
    normalized_bridge = normalize(bridge_region)
    normalized_theorem = normalize(theorem_region)
    print(f"BRIDGE REGION NORMALIZED LENGTH {len(normalized_bridge)}")
    print(f"THEOREM REGION NORMALIZED LENGTH {len(normalized_theorem)}")
    assert normalized_bridge == normalized_theorem, (
        "operational bridge and bridge-free theorem differ in cells/guards"
    )

    required_fragments = [
        '~>(Return(Name("result")).Stmts)~>#endcall',
        "<env>1=>0</env>",
        "<scopeLoc>2=>1</scopeLoc>",
        "<heapLoc>3</heapLoc>",
        "ListItem(frame(.K,0,1))=>.List",
        "<ret>noRet</ret>",
        "<exc>NoExc</exc>",
        "<exit-code>0</exit-code>",
        "requiresI>=Int0",
    ]
    for fragment in required_fragments:
        assert fragment in normalized_bridge, f"missing exact context fragment: {fragment}"
        print(f"CONTEXT FRAGMENT PRESENT {fragment}")

    print("NO-BRIDGE IMPORT ISOLATION true")
    print("BRIDGE/THEOREM COMPLETE CONTEXT IDENTITY true")


if __name__ == "__main__":
    main()
