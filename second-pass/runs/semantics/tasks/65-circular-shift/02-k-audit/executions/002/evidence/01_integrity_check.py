#!/usr/bin/env python3
"""Independent checks for launcher-owned provenance and mounted artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_records(root: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            kind = "symlink"
            payload: object = os.readlink(path)
        elif stat.S_ISREG(info.st_mode):
            kind = "file"
            payload = {"size": info.st_size, "sha256": sha256(path)}
        elif stat.S_ISDIR(info.st_mode):
            kind = "directory"
            payload = None
        else:
            kind = "other"
            payload = stat.S_IFMT(info.st_mode)
        records.append(
            {
                "path": relative,
                "kind": kind,
                "mode": stat.S_IMODE(info.st_mode),
                "payload": payload,
            }
        )
    return records


def canonical_digest(records: list[dict[str, object]]) -> str:
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    failures.append(message)


data = json.loads(AUDIT_INPUT.read_text())
failures: list[str] = []
print("record_layout:", data.get("record_layout"))
print("semantics_mode:", data.get("semantics_mode"))

if data.get("record_layout") != "legacy-selected-stage1":
    fail("unexpected record_layout")
if data.get("semantics_mode") != "SUPPLIED_SEMANTICS":
    fail("unexpected semantics_mode")

lock_path = Path(data["container_paths"]["audit_campaign_lock"])
lock_data = json.loads(lock_path.read_text())
if lock_data != data["audit_campaign"]:
    fail("campaign lock content does not exactly equal audit_input.audit_campaign")
else:
    print("OK: campaign lock content exactly equals audit_input.audit_campaign")

expected_files: dict[Path, str] = {
    lock_path: data["hashes"]["audit_campaign_lock_sha256"],
    Path(data["container_paths"]["run_manifest"]): data["hashes"]["run_manifest_sha256"],
    Path(data["container_paths"]["task_manifest"]): data["hashes"]["task_manifest_sha256"],
    Path(data["container_paths"]["stage1_result"]): data["hashes"]["stage1_result_sha256"],
    Path(data["container_paths"]["canonical"]): data["hashes"]["canonical_sha256"],
    Path(data["container_paths"]["trusted_prompt"]): data["hashes"]["trusted_prompt_sha256"],
    Path(data["container_paths"]["translator"]): data["hashes"]["trusted_translator_sha256"],
    Path(data["container_paths"]["generation_manifest"]): data["hashes"]["stage1_invocation_sha256"],
    Path(data["container_paths"]["generation_metrics"]): data["hashes"]["generation_metrics_sha256"],
    Path(data["container_paths"]["generation_last"]): data["hashes"]["generation_codex_last_sha256"],
    Path(data["container_paths"]["generation_output"]): data["hashes"]["generation_codex_output_sha256"],
    Path("/generation-evidence/prompt.txt"): data["hashes"]["generation_prompt_sha256"],
    Path("/generation-evidence/usage.json"): data["hashes"]["generation_usage_sha256"],
}

for path, expected in expected_files.items():
    if not path.exists():
        fail(f"missing required mounted file {path}")
        continue
    if path.is_symlink() or not path.is_file() or not os.access(path, os.R_OK):
        fail(f"required mounted file is not a readable non-symlink regular file: {path}")
        continue
    actual = sha256(path)
    if actual != expected:
        fail(f"hash mismatch {path}: expected={expected} actual={actual}")
    else:
        print(f"OK sha256 {actual} {path}")

generation_result = json.loads(Path("/generation-result.json").read_text())
declared_outputs = generation_result["outputs"]["evidence"]
for relative, expected in sorted(declared_outputs.items()):
    path = Path("/generation-evidence") / relative
    if not path.exists():
        fail(f"generation-result declares absent evidence file {path}")
        continue
    actual = sha256(path)
    if actual != expected:
        fail(f"generation-result evidence hash mismatch {path}: expected={expected} actual={actual}")
    else:
        print(f"OK stage1 evidence sha256 {actual} {path}")

required_layout_files = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_layout_files:
    if not path.exists() or not path.is_file() or path.is_symlink() or not os.access(path, os.R_OK):
        fail(f"required legacy-selected-stage1 record invalid: {path}")
print("OK: all required legacy-selected-stage1 records are readable regular non-symlink files")

for root in [Path("/candidate"), Path("/reference"), Path("/generation-evidence")]:
    records = tree_records(root)
    bad = [record for record in records if record["kind"] in {"symlink", "other"}]
    if bad:
        fail(f"non-regular/non-directory entries below {root}: {bad}")
    print(f"independent tree digest {canonical_digest(records)} {root}")
    print(f"tree record count {len(records)} {root}")
    for record in records:
        if record["kind"] == "file":
            payload = record["payload"]
            assert isinstance(payload, dict)
            print(
                f"TREE {root} {record['kind']} {record['mode']:04o} "
                f"{payload['size']} {payload['sha256']} {record['path']}"
            )
        else:
            print(f"TREE {root} {record['kind']} {record['mode']:04o} - - {record['path']}")

comparison_pairs = [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
]
for left, right, label in comparison_pairs:
    if left.is_symlink() or not left.is_file():
        fail(f"candidate {label} is missing, mistyped, or symlinked: {left}")
    elif left.read_bytes() != right.read_bytes():
        fail(f"candidate {label} differs from trusted input")
    else:
        print(f"OK: candidate {label} is byte-identical to trusted input")

candidate_semantics = tree_records(Path("/candidate/reference-semantics"))
trusted_semantics = tree_records(Path("/reference/reference-semantics"))
if candidate_semantics != trusted_semantics:
    fail("candidate reference-semantics tree differs in path, type, mode, size, or bytes")
else:
    print("OK: candidate reference-semantics recursively equals trusted tree")

print("recorded aggregate hashes (launcher algorithm not assumed):")
for key in sorted(data["hashes"]):
    print(f"RECORDED {key} {data['hashes'][key]}")

print("failure_count:", len(failures))
sys.exit(1 if failures else 0)
