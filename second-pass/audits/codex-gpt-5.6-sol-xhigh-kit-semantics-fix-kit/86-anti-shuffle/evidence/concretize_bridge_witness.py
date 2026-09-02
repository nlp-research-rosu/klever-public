#!/usr/bin/env python3
"""Remove unrelated symbolic state from the bridge counterexample claims."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("/tmp/audit-work/86-anti-shuffle")
EVIDENCE = Path("/audit-output/evidence")


def replace_exact(text: str, old: str, new: str, expected: int) -> str:
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"replacement count for {old!r}: expected {expected}, got {count}")
    return text.replace(old, new)


def main() -> int:
    source = (ROOT / "bridge-unsoundness-spec.k").read_text()
    concrete = source.replace("bridge-unsoundness-spec.k", "bridge-unsoundness-concrete-spec.k")
    concrete = replace_exact(concrete, "BASE:Map", ".Map", 6)
    concrete = replace_exact(concrete, "=> BASE\n    </scopes>", "=> .Map\n    </scopes>", 6)
    concrete = replace_exact(concrete, "<heap> HEAP:Map </heap>", "<heap> .Map </heap>", 6)
    concrete = replace_exact(concrete, "<heapLoc> NEXT:Int </heapLoc>", "<heapLoc> 0 </heapLoc>", 6)
    concrete = replace_exact(
        concrete,
        "ListItem(frame(CONT, 1, 2)) REST:List => REST",
        "ListItem(frame(.K, 1, 2)) => .List",
        3,
    )
    concrete = replace_exact(
        concrete,
        "ListItem(frame(CONT, 0, 1)) REST:List => REST",
        "ListItem(frame(.K, 0, 1)) => .List",
        3,
    )
    concrete = replace_exact(concrete, " ~> CONT:K", "", 6)
    scratch = ROOT / "bridge-unsoundness-concrete-spec.k"
    evidence = EVIDENCE / "bridge-unsoundness-concrete-spec.k"
    scratch.write_text(concrete)
    evidence.write_text(concrete)
    print(f"scratch={scratch}")
    print(f"evidence={evidence}")
    print("all six witnesses have concrete continuation, stack, heap, and surrounding scope map")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
