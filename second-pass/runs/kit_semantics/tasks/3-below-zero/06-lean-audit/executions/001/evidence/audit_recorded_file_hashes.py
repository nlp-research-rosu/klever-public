#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text())
recorded = audit_input["resolution"]["stage1_source_hashes"]
root = Path("/reference/k-proof")

missing = []
mismatched = []
for relative, expected in recorded.items():
    path = root / relative
    if not path.is_file():
        missing.append(relative)
        continue
    actual = sha256_file(path)
    if actual != expected:
        mismatched.append({"file": relative, "expected": expected, "actual": actual})

actual_files = {
    path.relative_to(root).as_posix()
    for path in root.rglob("*")
    if path.is_file() and not path.is_symlink()
}
recorded_files = set(recorded)

result = {
    "stage1_recorded_file_count": len(recorded),
    "stage1_actual_regular_file_count": len(actual_files),
    "missing_recorded_files": missing,
    "hash_mismatches": mismatched,
    "unrecorded_regular_files": sorted(actual_files - recorded_files),
    "recorded_paths_not_regular_files": sorted(recorded_files - actual_files),
    "all_recorded_stage1_hashes_match": not missing and not mismatched,
    "recorded_set_equals_regular_file_set": recorded_files == actual_files,
    "lean_invocation_recorded_path": audit_input["resolution"]["lean_invocation"],
    "lean_invocation_mounted_at_recorded_path": os.path.exists(
        audit_input["resolution"]["lean_invocation"]
    ),
    "note": (
        "The launcher did not mount the recorded Stage 5 invocation directory. "
        "Its historical transcript hash is therefore not an audit input; the mounted "
        "candidate tree and a fresh clean build were verified instead."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
