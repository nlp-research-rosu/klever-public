#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


CHUNK = 1024 * 1024


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hash(root: Path) -> str:
    """Reimplement the launcher tree digest from its public pipeline contract."""
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
                raise RuntimeError(f"unsupported linked/special entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(CHUNK):
                    digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def real_type(path: Path) -> str:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return "missing"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "special"


audit_path = Path("/audit-input.json")
audit = load_json(audit_path)
assert isinstance(audit, dict)
hashes = audit["hashes"]
assert isinstance(hashes, dict)

checks: list[tuple[str, bool, str]] = []


def check(name: str, passed: bool, detail: str = "") -> None:
    checks.append((name, passed, detail))


required_types = {
    "/audit-input.json": "file",
    "/audit-campaign-lock.json": "file",
    "/run.json": "file",
    "/task.json": "file",
    "/generation-result.json": "file",
    "/generation-evidence/invocation.json": "file",
    "/generation-evidence/metrics.json": "file",
    "/generation-evidence/codex-last.txt": "file",
    "/generation-evidence/codex-output.log": "file",
    "/generation-evidence/prompt.txt": "file",
    "/generation-evidence/codex-trace": "directory",
    "/candidate": "directory",
    "/reference/canonical.py": "file",
    "/reference/prompt.py": "file",
    "/reference/py2mpy.py": "file",
}
for raw_path, expected_type in required_types.items():
    actual_type = real_type(Path(raw_path))
    check(
        f"type {raw_path}",
        actual_type == expected_type,
        f"expected={expected_type} actual={actual_type}",
    )

check(
    "declared record layout",
    audit.get("record_layout") == "legacy-selected-stage1",
    str(audit.get("record_layout")),
)
check(
    "declared problem/condition/mode",
    (
        audit.get("problem_id") == "159-eat"
        and audit.get("condition") == "bare"
        and audit.get("semantics_mode") == "GENERATED_SEMANTICS"
    ),
    (
        f"problem={audit.get('problem_id')} condition={audit.get('condition')} "
        f"mode={audit.get('semantics_mode')}"
    ),
)
check(
    "GENERATED_SEMANTICS has no trusted reference-semantics mount",
    not Path("/reference/reference-semantics").exists()
    and not Path("/reference/reference-semantics").is_symlink(),
)

campaign = load_json(Path("/audit-campaign-lock.json"))
check(
    "campaign block equals campaign lock",
    campaign == audit.get("audit_campaign"),
)

expected_files = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
}
for key, path in expected_files.items():
    expected = hashes.get(key)
    actual = file_hash(path) if real_type(path) == "file" else None
    check(
        f"hash {key}",
        expected == actual,
        f"expected={expected} actual={actual}",
    )

result_record = load_json(Path("/generation-result.json"))
invocation_record = load_json(Path("/generation-evidence/invocation.json"))
usage_record = load_json(Path("/generation-evidence/usage.json"))
assert isinstance(result_record, dict)
assert isinstance(invocation_record, dict)
assert isinstance(usage_record, dict)

# The audit manifest does not specify the serialization used for its two
# aggregate tree hashes. Compute the independently documented pipeline-contract
# digest instead, pin it to the corresponding generation records, and print the
# audit aggregate so both values remain visible rather than falsely treating two
# different serializations as comparable.
candidate_pipeline_digest = tree_hash(Path("/candidate"))
candidate_generation_digest = (
    result_record.get("outputs", {}).get("workspace_sha256")
)
check(
    "candidate pipeline-contract tree digest matches generation result",
    candidate_pipeline_digest == candidate_generation_digest,
    (
        f"pipeline_digest={candidate_pipeline_digest} "
        f"generation_digest={candidate_generation_digest} "
        f"audit_recorded_aggregate={hashes.get('candidate_tree_sha256')}"
    ),
)
trace_pipeline_digest = tree_hash(Path("/generation-evidence/codex-trace"))
trace_generation_digest = usage_record.get("source_trace_sha256")
check(
    "trace pipeline-contract tree digest matches usage record",
    trace_pipeline_digest == trace_generation_digest,
    (
        f"pipeline_digest={trace_pipeline_digest} "
        f"usage_digest={trace_generation_digest} "
        f"audit_recorded_aggregate={hashes.get('generation_codex_trace_sha256')}"
    ),
)

check(
    "candidate prompt byte-identical to trusted prompt",
    Path("/candidate/prompt.py").read_bytes()
    == Path("/reference/prompt.py").read_bytes(),
)
check(
    "candidate translator byte-identical to trusted translator",
    Path("/candidate/py2mpy.py").read_bytes()
    == Path("/reference/py2mpy.py").read_bytes(),
)

for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    unsupported: list[str] = []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            unsupported.append(f"{real_type(path)}:{path}")
    check(
        f"no linked/special recursive entries in {root}",
        not unsupported,
        ", ".join(unsupported),
    )

for record in (
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/legacy-metrics.json"),
    Path("/generation-evidence/legacy-run-input.json"),
):
    try:
        load_json(record)
    except Exception as error:
        check(f"parse JSON {record}", False, repr(error))
    else:
        check(f"parse JSON {record}", True)

result = result_record
invocation = invocation_record
assert isinstance(result, dict) and isinstance(invocation, dict)
for owner, document in (("generation-result", result), ("invocation", invocation)):
    evidence = document.get("outputs", {}).get("evidence", {})
    assert isinstance(evidence, dict)
    for relative, expected in sorted(evidence.items()):
        path = Path("/generation-evidence") / relative
        actual_type = real_type(path)
        actual = file_hash(path) if actual_type == "file" else None
        check(
            f"{owner} evidence {relative}",
            actual_type == "file" and actual == expected,
            f"type={actual_type} expected={expected} actual={actual}",
        )

task = load_json(Path("/task.json"))
assert isinstance(task, dict)
task_inputs = task.get("inputs", {})
check(
    "task prompt hash pins trusted prompt",
    task_inputs.get("problem_prompt_sha256")
    == file_hash(Path("/reference/prompt.py")),
)
check(
    "task translator hash pins trusted translator",
    task_inputs.get("translator_sha256")
    == file_hash(Path("/reference/py2mpy.py")),
)
check(
    "task instruction hash pins generation prompt",
    task_inputs.get("instruction_prompt_sha256")
    == file_hash(Path("/generation-evidence/prompt.txt")),
)

for name, passed, detail in checks:
    suffix = f" :: {detail}" if detail else ""
    print(f"{'PASS' if passed else 'FAIL'} {name}{suffix}")

failed = sum(not passed for _, passed, _ in checks)
for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        print(
            f"FILE_SHA256 {file_hash(path)} "
            f"{path.relative_to(root).as_posix()} root={root}"
        )
print(f"SUMMARY checks={len(checks)} failed={failed}")
sys.exit(1 if failed else 0)
