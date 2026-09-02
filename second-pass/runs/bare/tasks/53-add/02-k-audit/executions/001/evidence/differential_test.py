#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import random
from pathlib import Path

SCRATCH = Path("/tmp/audit-work/53-add")
EVIDENCE = Path("/audit-output/evidence")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", SCRATCH / "trusted-canonical.py")
generated = load_module("generated_solution", SCRATCH / "solution.py")

documented = [(2, 3), (5, 7)]
zero_and_sign_boundaries = [
    (0, 0),
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
    (-1, 1),
    (1, -1),
    (-2, -3),
]
integer_magnitude_boundaries = [
    (2**63 - 1, 1),
    (-(2**63), -1),
    (2**63, -(2**63)),
    (10**100, -(10**100) + 7),
    (-(10**100), 10**100),
]

rng = random.Random(530053)
generated_small = [
    (rng.randint(-10**12, 10**12), rng.randint(-10**12, 10**12))
    for _ in range(256)
]
generated_wide = []
for _ in range(64):
    x = rng.getrandbits(512)
    y = rng.getrandbits(512)
    if rng.getrandbits(1):
        x = -x
    if rng.getrandbits(1):
        y = -y
    generated_wide.append((x, y))

groups = {
    "documented_examples": documented,
    "zero_and_sign_boundaries": zero_and_sign_boundaries,
    "integer_magnitude_boundaries": integer_magnitude_boundaries,
    "deterministic_generated_small": generated_small,
    "deterministic_generated_512_bit": generated_wide,
}
inputs_path = EVIDENCE / "differential-inputs.json"
inputs_path.write_text(json.dumps(groups, indent=2) + "\n")

mismatches = []
counts = {}
for group, cases in groups.items():
    counts[group] = len(cases)
    for x, y in cases:
        try:
            expected = ("return", canonical.add(x, y))
        except Exception as error:
            expected = ("exception", type(error).__name__, str(error))
        try:
            actual = ("return", generated.add(x, y))
        except Exception as error:
            actual = ("exception", type(error).__name__, str(error))
        if actual != expected:
            mismatches.append(
                {"group": group, "x": x, "y": y, "canonical": expected, "generated": actual}
            )

payload = inputs_path.read_bytes()
print("ORACLE: trusted canonical add imported from scratch copy of /reference/canonical.py")
print("SUBJECT: generated add imported from scratch copy of /candidate/solution.py")
print("FORMAL_INPUT_DOMAIN: pairs of Python int values")
print("BRANCH_BOUNDARIES: none; both implementations are branch-free")
print("EMPTY_CASES: not applicable to scalar integer parameters; additive zero cases used")
print(f"GROUP_COUNTS: {json.dumps(counts, sort_keys=True)}")
print(f"TOTAL_CASES: {sum(counts.values())}")
print(f"INPUT_FILE: {inputs_path}")
print(f"INPUT_SHA256: {hashlib.sha256(payload).hexdigest()}")
print(f"MISMATCH_COUNT: {len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH: {json.dumps(mismatch, sort_keys=True)}")
raise SystemExit(1 if mismatches else 0)
