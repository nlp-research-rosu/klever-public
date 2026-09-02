#!/usr/bin/env python3
"""Independent integrity checks for the launcher mounts used by this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reviewer_tree_hash(root: Path) -> str:
    """A documented reviewer-local tree digest, independent of launcher code."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode()
        mode = path.lstat().st_mode
        kind = b"L" if stat.S_ISLNK(mode) else b"F" if stat.S_ISREG(mode) else b"D"
        digest.update(kind + b"\0" + relative + b"\0")
        if kind == b"L":
            digest.update(os.readlink(path).encode() + b"\0")
        elif kind == b"F":
            digest.update(bytes.fromhex(sha256(path)))
    return digest.hexdigest()


audit = json.loads(AUDIT.read_text())
lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
lock = json.loads(lock_path.read_text())

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_json_equal={lock == audit['audit_campaign']}")
actual_lock_hash = sha256(lock_path)
expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"audit_campaign_lock expected={expected_lock_hash} actual={actual_lock_hash}")
assert actual_lock_hash == expected_lock_hash
assert lock == audit["audit_campaign"]

required = {
    "audit_input": Path("/audit-input.json"),
    "audit_campaign_lock": lock_path,
    "run_manifest": Path(audit["container_paths"]["run_manifest"]),
    "task_manifest": Path(audit["container_paths"]["task_manifest"]),
    "stage1_result": Path(audit["container_paths"]["stage1_result"]),
    "generation_invocation": Path(audit["container_paths"]["generation_manifest"]),
    "generation_metrics": Path(audit["container_paths"]["generation_metrics"]),
    "generation_last": Path(audit["container_paths"]["generation_last"]),
    "generation_output": Path(audit["container_paths"]["generation_output"]),
    "generation_prompt": Path("/generation-evidence/prompt.txt"),
    "generation_usage": Path("/generation-evidence/usage.json"),
    "generation_trace": Path(audit["container_paths"]["generation_trace"]),
    "candidate": Path(audit["container_paths"]["candidate"]),
    "canonical": Path(audit["container_paths"]["canonical"]),
    "trusted_prompt": Path(audit["container_paths"]["trusted_prompt"]),
    "translator": Path(audit["container_paths"]["translator"]),
}

for name, path in required.items():
    mode = path.lstat().st_mode
    assert not stat.S_ISLNK(mode), f"required path is symlink: {path}"
    expected_kind = "directory" if name in {"generation_trace", "candidate"} else "file"
    actual_kind = "directory" if stat.S_ISDIR(mode) else "file" if stat.S_ISREG(mode) else "other"
    print(f"required {name}: {path} kind={actual_kind}")
    assert actual_kind == expected_kind

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert not Path("/reference/reference-semantics").exists()
print("trusted_reference_semantics_absent=True")

for tree in (Path("/candidate"), Path("/generation-evidence/codex-trace"), Path("/reference")):
    symlinks = [str(path) for path in tree.rglob("*") if path.is_symlink()]
    print(f"symlinks {tree}: {symlinks}")
    assert not symlinks
    print(f"reviewer_tree_sha256 {tree}: {reviewer_tree_hash(tree)}")

checks = {
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
}

for key, path in checks.items():
    expected = audit["hashes"][key]
    actual = sha256(path)
    print(f"hash {key}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identity=True")
print("candidate_translator_byte_identity=True")

result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    assert path.is_file() and not path.is_symlink()
    actual = sha256(path)
    print(f"stage1_leaf {relative}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

trace_lines = 0
for path in sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl")):
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            json.loads(line)
            trace_lines += 1
print(f"structured_trace_json_lines={trace_lines}")
assert trace_lines > 0

proof_artifacts = [
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
]
for relative in proof_artifacts:
    path = Path("/candidate") / relative
    assert path.is_file() and not path.is_symlink()
    print(f"candidate_artifact {relative}: sha256={sha256(path)}")

print("PROVENANCE_CHECK=PASS")
