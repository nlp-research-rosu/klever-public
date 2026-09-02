#!/usr/bin/env python3
"""Read-only launcher provenance and digest checks used by the audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce pipeline_contract.sha256_tree without importing launcher code."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise RuntimeError(f"not a real directory: {root}")
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["audit_campaign"] == lock

checks = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
}

failures = 0
for key, path in checks.items():
    if not stat.S_ISREG(path.lstat().st_mode):
        print(f"{key}: ok=False path is not a real regular file: {path}")
        failures += 1
        continue
    actual = file_hash(path)
    expected = audit["hashes"][key]
    ok = actual == expected
    failures += not ok
    print(f"{key}: ok={ok} expected={expected} actual={actual} path={path}")

result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    real_regular = stat.S_ISREG(path.lstat().st_mode)
    actual = file_hash(path) if real_regular else "<unsupported>"
    ok = real_regular and actual == expected
    failures += not ok
    print(
        f"generation_result_evidence[{relative}]: ok={ok} "
        f"expected={expected} actual={actual} path={path}"
    )

print(f"campaign_object_equal={audit['audit_campaign'] == lock}")
print(f"candidate_prompt_byte_equal={Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}")
print(f"candidate_translator_byte_equal={Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}")
print(f"trusted_reference_semantics_absent={not Path('/reference/reference-semantics').exists()}")

candidate_tree = pipeline_tree_hash(Path("/candidate"))
trace_tree = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
print(f"candidate_pipeline_tree_hash={candidate_tree}")
print(f"candidate_invocation_workspace_hash={invocation['outputs']['workspace_sha256']}")
print(f"candidate_pipeline_tree_matches_invocation={candidate_tree == invocation['outputs']['workspace_sha256']}")
print(f"trace_pipeline_tree_hash={trace_tree}")
print(f"trace_usage_source_hash={usage['source_trace_sha256']}")
print(f"trace_pipeline_tree_matches_usage={trace_tree == usage['source_trace_sha256']}")

raise SystemExit(failures)
