#!/usr/bin/env python3
"""Check the required final pair and core audit evidence."""

from pathlib import Path


review = Path("/audit-output/REVIEW.md").read_text()
final_pair = "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
assert review.endswith(final_pair)
assert review.count("\nVERDICT:") == 1
assert review.count("\nLEGITIMACY:") == 1

required = {
    "audit-input-and-mode.log",
    "producer-source-hashes.log",
    "producer-bundle-artifact-hash.log",
    "reconstructed-rule-inventory.log",
    "stage3-bijection-validation.log",
    "frozen-source-and-semantics.log",
    "k-count-hook-semantics.log",
    "hash-audit.log",
    "fresh-klean-preflight.log",
    "lean-environment-shim-validation.log",
    "fresh-klean-preflight-success.log",
    "stage4-manifests-and-target.log",
    "stage4-structure-audit.log",
}
evidence = Path("/audit-output/evidence")
missing = sorted(name for name in required if not (evidence / name).is_file())
assert not missing, missing

print("FINAL PAIR: EXACT AND UNIQUE")
print("REQUIRED EVIDENCE FILES: PRESENT")
print(final_pair, end="")
