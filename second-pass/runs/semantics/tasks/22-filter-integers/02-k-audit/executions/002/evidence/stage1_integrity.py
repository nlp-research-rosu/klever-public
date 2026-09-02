#!/usr/bin/env python3
"""Independent launcher/provenance checks for the 22-filter-integers audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert path.is_file(), f"not regular: {path}"
    assert not path.is_symlink(), f"symlinked: {path}"
    with path.open("rb") as stream:
        stream.read(1)


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
generation_result_document = json.loads(Path("/generation-result.json").read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert lock == audit["audit_campaign"]
print("campaign_block_match=true")

required = [
    AUDIT_INPUT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    required.append(usage)
legacy_metrics = Path("/generation-evidence/legacy-metrics.json")
legacy_run_input = Path("/generation-evidence/legacy-run-input.json")
for optional_record in (legacy_metrics, legacy_run_input):
    if optional_record.exists():
        required.append(optional_record)
for path in required:
    require_regular(path)
print(f"required_regular_files={len(required)}")

trace_root = Path(audit["container_paths"]["generation_trace"])
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_files = sorted(trace_root.rglob("*.jsonl"))
assert trace_files
trace_records = 0
for path in trace_files:
    require_regular(path)
    for number, line in enumerate(path.read_text().splitlines(), 1):
        json.loads(line)
        trace_records += 1
print(f"trace_files={len(trace_files)} trace_records={trace_records}")

expected_hashes = {
    LOCK: audit["hashes"]["audit_campaign_lock_sha256"],
    Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
    Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
    Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
    Path("/generation-evidence/invocation.json"): audit["hashes"]["stage1_invocation_sha256"],
    Path("/generation-evidence/metrics.json"): audit["hashes"]["generation_metrics_sha256"],
    Path("/generation-evidence/codex-last.txt"): audit["hashes"]["generation_codex_last_sha256"],
    Path("/generation-evidence/codex-output.log"): audit["hashes"]["generation_codex_output_sha256"],
    Path("/generation-evidence/prompt.txt"): audit["hashes"]["generation_prompt_sha256"],
    Path("/reference/canonical.py"): audit["hashes"]["canonical_sha256"],
    Path("/reference/prompt.py"): audit["hashes"]["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): audit["hashes"]["trusted_translator_sha256"],
}
if usage.exists():
    expected_hashes[usage] = audit["hashes"]["generation_usage_sha256"]
generation_evidence_hashes = generation_result_document["outputs"]["evidence"]
if legacy_metrics.exists():
    expected_hashes[legacy_metrics] = generation_evidence_hashes["legacy-metrics.json"]
if legacy_run_input.exists():
    expected_hashes[legacy_run_input] = generation_evidence_hashes[
        "legacy-run-input.json"
    ]
for path, expected in expected_hashes.items():
    actual = digest(path)
    assert actual == expected, f"hash mismatch: {path}: {actual} != {expected}"
    print(f"sha256 {actual} {path}")

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identical=true")
print("candidate_translator_byte_identical=true")


def tree_manifest(root: Path) -> list[tuple[str, str, str]]:
    assert root.is_dir() and not root.is_symlink()
    result = []
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root))
        assert not path.is_symlink(), f"symlinked tree entry: {path}"
        if path.is_dir():
            result.append(("d", relative, ""))
        elif path.is_file():
            result.append(("f", relative, digest(path)))
        else:
            raise AssertionError(f"non-file tree entry: {path}")
    return result


trusted_manifest = tree_manifest(Path("/reference/reference-semantics"))
candidate_manifest = tree_manifest(Path("/candidate/reference-semantics"))
assert candidate_manifest == trusted_manifest
file_count = sum(kind == "f" for kind, _, _ in trusted_manifest)
directory_count = sum(kind == "d" for kind, _, _ in trusted_manifest)
print(f"reference_semantics_tree_identical=true files={file_count} directories={directory_count}")


def tree_digest(root: Path) -> str:
    """Reimplement the launcher tree hash over path, kind, size, and content."""
    assert root.is_dir() and not root.is_symlink()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    h = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
        h.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            h.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(block)
    return h.hexdigest()


invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
usage_document = json.loads(usage.read_text()) if usage.exists() else {}
tree_expectations = {
    # These records use the launcher manifest-tree algorithm reimplemented
    # above. /audit-input.json also carries secondary content/tree digests from
    # legacy import; exact recursive comparison and per-file hashes cover those.
    Path("/candidate"): invocation["retained_workspace_sha256"],
    Path("/candidate/reference-semantics"): audit["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ],
    Path("/reference/reference-semantics"): audit["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ],
    trace_root: usage_document["source_trace_sha256"],
}
for root, expected in tree_expectations.items():
    actual = tree_digest(root)
    assert actual == expected, f"tree hash mismatch: {root}: {actual} != {expected}"
    print(f"tree_sha256 {actual} {root}")
assert (
    tree_digest(Path("/candidate"))
    == generation_result_document["outputs"]["workspace_sha256"]
)
print(
    "recorded_secondary_hashes_inspected="
    f"candidate:{audit['hashes']['candidate_tree_sha256']},"
    f"candidate_semantics:{audit['hashes']['candidate_reference_semantics_sha256']},"
    f"trusted_semantics:{audit['hashes']['trusted_reference_semantics_sha256']},"
    f"trace:{audit['hashes']['generation_codex_trace_sha256']}"
)

print("stage1_integrity=PASS")
