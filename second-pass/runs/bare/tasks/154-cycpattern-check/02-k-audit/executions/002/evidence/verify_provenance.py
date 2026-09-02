#!/usr/bin/env python3
"""Independent integrity/readability checks for launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce the recorded pipeline tree digest from entry names and bytes."""
    result = hashlib.sha256()
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
                raise RuntimeError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        result.update(len(encoded).to_bytes(4, "big"))
        result.update(encoded)
        result.update(kind.encode() + b"\0")
        if kind == "file":
            result.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            result.update(path.read_bytes())
    return result.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
errors: list[str] = []

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")

if audit["record_layout"] != "legacy-selected-stage1":
    errors.append("unexpected record layout")
if audit["semantics_mode"] != "GENERATED_SEMANTICS":
    errors.append("unexpected semantics mode")
if lock != audit["audit_campaign"]:
    errors.append("campaign lock JSON does not equal audit_campaign block")
print(f"campaign_block_equal={lock == audit['audit_campaign']}")

declared_paths = {
    key: Path(value) for key, value in audit["container_paths"].items()
}
for key, path in sorted(declared_paths.items()):
    exists = path.exists()
    readable = os.access(path, os.R_OK)
    print(
        f"container_path key={key} path={path} "
        f"exists={exists} readable={readable}"
    )
    if not exists or not readable:
        errors.append(f"missing/unreadable declared mount: {key}={path}")

required_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_records:
    if not path.is_file() or not os.access(path, os.R_OK):
        errors.append(f"required record missing/unreadable: {path}")
    else:
        # Read the entire record; JSON records are also parsed below.
        contents = path.read_bytes()
        print(
            f"required_record path={path} bytes={len(contents)} "
            f"sha256={hashlib.sha256(contents).hexdigest()}"
        )

json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/legacy-metrics.json"),
    Path("/generation-evidence/legacy-run-input.json"),
]
for path in json_records:
    parsed = json.loads(path.read_text(encoding="utf-8"))
    print(f"json_parsed path={path} top_type={type(parsed).__name__}")

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*"))
trace_regular = [path for path in trace_files if path.is_file()]
if not trace_regular:
    errors.append("structured trace has no regular files")
trace_records = 0
for path in trace_regular:
    relative = path.relative_to(trace_root)
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        json.loads(line)
    trace_records += len(lines)
    print(
        f"trace_file path={relative} records={len(lines)} "
        f"sha256={digest(path)}"
    )
print(f"trace_total_records={trace_records}")

expected_hashes = {
    Path("/audit-campaign-lock.json"): audit["hashes"]["audit_campaign_lock_sha256"],
    Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
    Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
    Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
    Path("/generation-evidence/invocation.json"): audit["hashes"]["stage1_invocation_sha256"],
    Path("/generation-evidence/metrics.json"): audit["hashes"]["generation_metrics_sha256"],
    Path("/generation-evidence/usage.json"): audit["hashes"]["generation_usage_sha256"],
    Path("/generation-evidence/codex-last.txt"): audit["hashes"]["generation_codex_last_sha256"],
    Path("/generation-evidence/codex-output.log"): audit["hashes"]["generation_codex_output_sha256"],
    Path("/generation-evidence/prompt.txt"): audit["hashes"]["generation_prompt_sha256"],
    Path("/reference/canonical.py"): audit["hashes"]["canonical_sha256"],
    Path("/reference/prompt.py"): audit["hashes"]["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): audit["hashes"]["trusted_translator_sha256"],
    Path("/candidate/prompt.py"): audit["hashes"]["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): audit["hashes"]["candidate_translator_sha256"],
}
for path, expected in expected_hashes.items():
    actual = digest(path)
    ok = actual == expected
    print(
        f"declared_hash path={path} expected={expected} actual={actual} "
        f"match={ok}"
    )
    if not ok:
        errors.append(f"hash mismatch: {path}")

result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
for relative, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    actual = digest(path)
    ok = actual == expected
    print(
        f"result_evidence_hash path={path} expected={expected} actual={actual} "
        f"match={ok}"
    )
    if not ok:
        errors.append(f"generation-result evidence hash mismatch: {path}")

candidate_pipeline_hash = pipeline_tree_digest(Path("/candidate"))
expected_workspace_hashes = {
    result["outputs"]["workspace_sha256"],
    json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )["retained_workspace_sha256"],
}
candidate_pipeline_match = expected_workspace_hashes == {candidate_pipeline_hash}
print(
    f"candidate_pipeline_tree_sha256={candidate_pipeline_hash} "
    f"recorded={sorted(expected_workspace_hashes)} "
    f"match={candidate_pipeline_match}"
)
if not candidate_pipeline_match:
    errors.append("candidate pipeline tree digest mismatch")

trace_pipeline_hash = pipeline_tree_digest(trace_root)
usage = json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)
trace_pipeline_match = trace_pipeline_hash == usage["source_trace_sha256"]
print(
    f"trace_pipeline_tree_sha256={trace_pipeline_hash} "
    f"recorded={usage['source_trace_sha256']} match={trace_pipeline_match}"
)
if not trace_pipeline_match:
    errors.append("trace pipeline tree digest mismatch")

candidate_required = [
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "solution-program.k",
    "verification.k",
    "spec.k",
    "prove.sh",
    "build_solution_k.py",
    "prompt.py",
    "py2mpy.py",
]
for name in candidate_required:
    path = Path("/candidate") / name
    ok = path.is_file() and not path.is_symlink() and os.access(path, os.R_OK)
    print(f"candidate_artifact path={path} regular_readable_nonsymlink={ok}")
    if not ok:
        errors.append(f"candidate proof artifact defect: {path}")

scan_roots = [
    Path("/candidate"),
    Path("/reference"),
    Path("/generation-evidence"),
]
symlinks = [
    path for root in scan_roots for path in root.rglob("*") if path.is_symlink()
]
print(f"symlink_count={len(symlinks)}")
for path in symlinks:
    print(f"symlink path={path} target={os.readlink(path)}")

prompt_equal = (
    Path("/candidate/prompt.py").read_bytes()
    == Path("/reference/prompt.py").read_bytes()
)
translator_equal = (
    Path("/candidate/py2mpy.py").read_bytes()
    == Path("/reference/py2mpy.py").read_bytes()
)
print(f"candidate_prompt_byte_equal_trusted={prompt_equal}")
print(f"candidate_translator_byte_equal_trusted={translator_equal}")
if not prompt_equal:
    errors.append("candidate prompt differs from trusted prompt")
if not translator_equal:
    errors.append("candidate translator differs from trusted translator")

trusted_semantics_absent = not Path("/reference/reference-semantics").exists()
candidate_reference_semantics_absent = not Path(
    "/candidate/reference-semantics"
).exists()
print(f"trusted_reference_semantics_absent={trusted_semantics_absent}")
print(
    "candidate_reference_semantics_absent="
    f"{candidate_reference_semantics_absent}"
)
if not trusted_semantics_absent:
    errors.append("GENERATED_SEMANTICS contradicted by trusted semantics mount")

for root in [Path("/candidate"), Path("/reference")]:
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        print(
            f"independent_file_hash path={path} bytes={path.stat().st_size} "
            f"sha256={digest(path)}"
        )

print(f"error_count={len(errors)}")
for error in errors:
    print(f"ERROR: {error}")
raise SystemExit(1 if errors else 0)
