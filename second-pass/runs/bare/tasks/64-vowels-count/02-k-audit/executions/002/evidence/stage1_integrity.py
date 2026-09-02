#!/usr/bin/env python3
"""Independent launcher-record and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def real_directory(path: Path) -> bool:
    return path.is_dir() and not path.is_symlink()


def tree_manifest(root: Path) -> tuple[list[dict[str, object]], str]:
    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISLNK(mode):
            kind = "symlink"
            record: dict[str, object] = {
                "path": relative,
                "kind": kind,
                "target": os.readlink(path),
            }
        elif stat.S_ISDIR(mode):
            record = {"path": relative, "kind": "directory"}
        elif stat.S_ISREG(mode):
            record = {
                "path": relative,
                "kind": "file",
                "size": path.stat().st_size,
                "sha256": sha256(path),
            }
        else:
            record = {"path": relative, "kind": "unsupported"}
        records.append(record)
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return records, hashlib.sha256(encoded).hexdigest()


audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
campaign_lock = json.loads(LOCK.read_text(encoding="utf-8"))
expected_hashes = audit_input["hashes"]

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"condition={audit_input['condition']}")

assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit_input["mount_reference_semantics"] is False
assert campaign_lock == audit_input["audit_campaign"]
print("campaign_object_matches=true")

lock_observed = sha256(LOCK)
lock_expected = expected_hashes["audit_campaign_lock_sha256"]
print(f"audit_campaign_lock expected={lock_expected} observed={lock_observed}")
assert lock_observed == lock_expected

required_files = [
    AUDIT_INPUT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
required_directories = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_files:
    assert regular(path), f"missing, unreadable, linked, or mistyped required file: {path}"
    print(f"regular_file=true path={path}")
for path in required_directories:
    assert real_directory(path), f"missing, unreadable, linked, or mistyped directory: {path}"
    print(f"real_directory=true path={path}")

usage = Path("/generation-evidence/usage.json")
assert regular(usage)
print(f"optional_usage_present=true path={usage}")

assert not Path("/reference/reference-semantics").exists()
assert not Path("/candidate/reference-semantics").exists()
print("trusted_reference_semantics_absent=true")
print("candidate_reference_semantics_absent=true")

checks = [
    (LOCK, "audit_campaign_lock_sha256"),
    (Path("/reference/canonical.py"), "canonical_sha256"),
    (Path("/reference/prompt.py"), "trusted_prompt_sha256"),
    (Path("/reference/py2mpy.py"), "trusted_translator_sha256"),
    (Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
    (Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
    (Path("/run.json"), "run_manifest_sha256"),
    (Path("/task.json"), "task_manifest_sha256"),
    (Path("/generation-result.json"), "stage1_result_sha256"),
    (Path("/generation-evidence/invocation.json"), "stage1_invocation_sha256"),
    (Path("/generation-evidence/metrics.json"), "generation_metrics_sha256"),
    (usage, "generation_usage_sha256"),
    (Path("/generation-evidence/codex-last.txt"), "generation_codex_last_sha256"),
    (Path("/generation-evidence/codex-output.log"), "generation_codex_output_sha256"),
    (Path("/generation-evidence/prompt.txt"), "generation_prompt_sha256"),
]
for path, key in checks:
    expected = expected_hashes[key]
    observed = sha256(path)
    print(f"{key} expected={expected} observed={observed} match={expected == observed}")
    assert observed == expected

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identity=true")
print("candidate_translator_byte_identity=true")

for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    records, independent_hash = tree_manifest(root)
    print(f"independent_tree_manifest root={root} sha256={independent_hash}")
    for record in records:
        print(json.dumps(record, sort_keys=True))
    assert all(record["kind"] in {"directory", "file"} for record in records)

print("STAGE1_INTEGRITY_OK")
