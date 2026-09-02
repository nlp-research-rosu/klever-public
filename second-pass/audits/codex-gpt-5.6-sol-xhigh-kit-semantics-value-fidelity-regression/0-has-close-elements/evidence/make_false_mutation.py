#!/usr/bin/env python3
"""Create and preserve a fresh false result mutation of the audited entry claim."""

from __future__ import annotations

import shutil
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
EVIDENCE = Path("/audit-output/evidence")


def main() -> int:
    original = (WORK / "spec.k").read_text()
    if original.count("module SPEC\n") != 1:
        raise RuntimeError("unexpected SPEC module declaration")
    target_start = original.index("  claim [target]:")
    prefix = original[:target_start]
    target = original[target_start:]
    original_result = "outerAcc(false, 0, INPUT, INPUT, THRESHOLD)"
    if target.count(original_result) != 1:
        raise RuntimeError("unexpected target-result occurrence count")
    mutated = (
        prefix.replace("module SPEC\n", "module AUDIT-FALSE-SPEC\n", 1)
        + target.replace(original_result, "true", 1)
    )
    scratch_path = WORK / "audit-false-spec.k"
    evidence_path = EVIDENCE / "audit-false-spec.k"
    scratch_path.write_text(mutated)
    shutil.copyfile(scratch_path, evidence_path)
    print(f"original_result={original_result}")
    print("mutated_result=true")
    print("satisfying_counterexample=INPUT:.FloatSeq, THRESHOLD:0.5")
    print("expected_original_result=false")
    print(f"scratch_mutation={scratch_path}")
    print(f"preserved_mutation={evidence_path}")
    print(f"mutation_bytes={scratch_path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
