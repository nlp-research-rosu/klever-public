#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


def load_entry(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


def main() -> int:
    evidence_dir = Path(__file__).resolve().parent
    inputs_path = evidence_dir / "differential_inputs.json"
    scratch = Path("/tmp/audit-work/fresh")
    canonical = load_entry("trusted_canonical", scratch / "canonical.py")
    candidate = load_entry("candidate_solution", scratch / "solution.py")
    groups = json.loads(inputs_path.read_text(encoding="utf-8"))

    all_inputs = []
    for group, values in groups.items():
        print(f"GROUP {group}: {values}")
        all_inputs.extend(values)

    seen = set()
    ordered_inputs = []
    for value in all_inputs:
        if value not in seen:
            seen.add(value)
            ordered_inputs.append(value)

    mismatches = []
    digest = hashlib.sha256()
    for n in ordered_inputs:
        expected = canonical(n)
        actual = candidate(n)
        digest.update(repr((n, expected, actual)).encode("utf-8"))
        if expected != actual:
            mismatches.append((n, expected, actual))
        if n in {-5, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 20}:
            print(f"CASE n={n}: canonical={expected!r} candidate={actual!r}")
        else:
            print(
                f"CASE n={n}: length={len(actual)} "
                f"last={actual[-1] if actual else None!r} match={expected == actual}"
            )

    print(f"TOTAL_CASES: {len(ordered_inputs)}")
    print(f"MISMATCH_COUNT: {len(mismatches)}")
    print(f"RESULT_DIGEST_SHA256: {digest.hexdigest()}")
    for mismatch in mismatches:
        print(f"MISMATCH: {mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
