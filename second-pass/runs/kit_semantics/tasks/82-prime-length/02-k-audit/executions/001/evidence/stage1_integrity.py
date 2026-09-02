#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlinked: {path}"
    assert path.is_file(), f"not a regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())

assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["mount_reference_semantics"] is True
assert lock == audit["audit_campaign"]
assert digest(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
print("campaign block: exact JSON match")
print(f"audit campaign lock sha256: {digest(LOCK)} MATCH")

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
for path in required:
    require_regular(path)
print(f"required regular/readable records: {len(required)}")

declared_hashes = {
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
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
for raw_path, key in declared_hashes.items():
    path = Path(raw_path)
    require_regular(path)
    actual = digest(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"hash mismatch {path}: {actual} != {expected}"
    print(f"{path}: {actual} MATCH {key}")

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    require_regular(path)
    actual = digest(path)
    assert actual == expected, f"stage1 evidence mismatch {path}"
    print(f"stage1 evidence {rel}: {actual} MATCH")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_regular = [p for p in trace_files if p.is_file() and not p.is_symlink()]
assert trace_regular, "structured trace has no regular files"
assert not any(p.is_symlink() for p in trace_files), "symlink in structured trace"
trace_lines = 0
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
for path in trace_regular:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            assert isinstance(record, dict)
            trace_lines += 1
            top_types[str(record.get("type", "<none>"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type", "<none>"))] += 1
    print(f"structured trace parsed: {path} ({line_number} JSON records)")
print(f"structured trace total records: {trace_lines}")
print(f"structured trace top-level types: {dict(sorted(top_types.items()))}")
print(f"structured trace payload types: {dict(sorted(payload_types.items()))}")

candidate_semantics = Path("/candidate/reference-semantics")
trusted_semantics = Path("/reference/reference-semantics")
assert candidate_semantics.is_dir() and not candidate_semantics.is_symlink()
assert trusted_semantics.is_dir() and not trusted_semantics.is_symlink()


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[rel] = ("symlink", os.readlink(path))
        elif path.is_dir():
            result[rel] = ("directory", None)
        elif path.is_file():
            result[rel] = ("file", digest(path))
        else:
            result[rel] = ("other", None)
    return result


def reviewer_tree_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    """Reviewer-defined digest over path, node type, and file digest."""
    h = hashlib.sha256()
    for rel, (kind, value) in sorted(entries.items()):
        h.update(rel.encode())
        h.update(b"\0")
        h.update(kind.encode())
        h.update(b"\0")
        if value is not None:
            h.update(value.encode())
        h.update(b"\0")
    return h.hexdigest()


candidate_tree = tree(candidate_semantics)
trusted_tree = tree(trusted_semantics)
assert candidate_tree == trusted_tree, "candidate supplied-semantics tree differs"
assert all(kind != "symlink" for kind, _ in candidate_tree.values())
file_count = sum(kind == "file" for kind, _ in candidate_tree.values())
directory_count = sum(kind == "directory" for kind, _ in candidate_tree.values())
print(
    "supplied semantics recursive type/path/byte comparison: "
    f"MATCH ({file_count} files, {directory_count} directories, 0 symlinks)"
)
print(
    "reviewer supplied-semantics tree digest: "
    f"{reviewer_tree_digest(candidate_tree)}"
)

proof_required = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for name in proof_required:
    path = Path("/candidate") / name
    require_regular(path)
    print(f"candidate proof source {name}: {digest(path)}")
print(f"required candidate proof artifacts: {len(proof_required)} regular files")

all_candidate_tree = tree(Path("/candidate"))
print(
    "reviewer full-candidate tree digest: "
    f"{reviewer_tree_digest(all_candidate_tree)} "
    f"({len(all_candidate_tree)} entries)"
)
print("STAGE1_INTEGRITY: PASS")
