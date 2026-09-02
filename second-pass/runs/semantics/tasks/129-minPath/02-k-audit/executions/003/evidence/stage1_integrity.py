#!/usr/bin/env python3
"""Independent integrity checks over the container-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = str(path.relative_to(root))
            if path.is_symlink():
                result[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                result[rel] = ("dir", None)
            elif path.is_file():
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = ("other", None)
    return result


audit = json.loads(Path("/audit-input.json").read_text())
lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
lock = json.loads(lock_path.read_text())
print("record_layout:", audit["record_layout"])
print("semantics_mode:", audit["semantics_mode"])
print("campaign_block_equals_lock:", audit["audit_campaign"] == lock)
print("campaign_lock_sha256:", sha256(lock_path))
print("campaign_lock_hash_matches:", sha256(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"])

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
]
print("required_records:")
for path in required:
    print(f"  {path}: present={path.exists()} readable={os.access(path, os.R_OK)} symlink={path.is_symlink()}")

checks = {
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
}
print("declared_file_hash_checks:")
for raw_path, key in checks.items():
    path = Path(raw_path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"  {raw_path}: actual={actual} expected={expected} match={actual == expected}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
print("trace_files:", len(trace_files))
for path in trace_files:
    print(f"  {path}: sha256={sha256(path)}")

trusted_semantics = inventory(Path("/reference/reference-semantics"))
candidate_semantics = inventory(Path("/candidate/reference-semantics"))
print("trusted_semantics_entries:", len(trusted_semantics))
print("candidate_semantics_entries:", len(candidate_semantics))
print("semantics_inventories_identical:", trusted_semantics == candidate_semantics)
print("trusted_semantics_symlinks:", [p for p, item in trusted_semantics.items() if item[0] == "symlink"])
print("candidate_semantics_symlinks:", [p for p, item in candidate_semantics.items() if item[0] == "symlink"])
if trusted_semantics != candidate_semantics:
    keys = sorted(set(trusted_semantics) | set(candidate_semantics))
    for key in keys:
        if trusted_semantics.get(key) != candidate_semantics.get(key):
            print("SEMANTICS_MISMATCH", key, trusted_semantics.get(key), candidate_semantics.get(key))

print("candidate_prompt_byte_identical:", Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes())
print("candidate_translator_byte_identical:", Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes())

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
assert all(path.exists() and os.access(path, os.R_OK) and not path.is_symlink() for path in required)
assert all(sha256(Path(path)) == audit["hashes"][key] for path, key in checks.items())
assert trusted_semantics == candidate_semantics
assert not any(item[0] == "symlink" for item in trusted_semantics.values())
assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("STAGE1_INTEGRITY: PASS")
