#!/usr/bin/env python3
"""Independent integrity checks over launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
document = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
metrics = json.loads(Path("/generation-evidence/metrics.json").read_text())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the recorded pipeline workspace-tree algorithm."""
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError(f"not a real directory: {root}")
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
                raise RuntimeError(f"linked or unsupported entry: {path}")
    digest = hashlib.sha256()
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


required = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
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
    Path("/generation-evidence/usage.json"),
]
for path in required:
    mode = path.lstat().st_mode
    print(
        f"required={path} regular={stat.S_ISREG(mode)} "
        f"symlink={stat.S_ISLNK(mode)} readable={os.access(path, os.R_OK)}"
    )

print(f"record_layout={document['record_layout']}")
print(f"semantics_mode={document['semantics_mode']}")
print(f"campaign_block_equal={document['audit_campaign'] == lock}")
print(
    "campaign_lock_hash="
    f"{sha256_file(Path('/audit-campaign-lock.json'))} "
    f"recorded={document['hashes']['audit_campaign_lock_sha256']}"
)
print(
    "reference_semantics_present="
    f"{Path('/reference/reference-semantics').exists()}"
)

hash_checks = {
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
}
for key, path in hash_checks.items():
    actual = sha256_file(path)
    recorded = document["hashes"][key]
    print(f"hash={key} actual={actual} recorded={recorded} match={actual == recorded}")

print(
    "candidate_prompt_byte_equal="
    f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
)
print(
    "candidate_translator_byte_equal="
    f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
)

trace_files = sorted(
    path for path in Path("/generation-evidence/codex-trace").rglob("*")
    if path.is_file()
)
for path in trace_files:
    relative = path.relative_to("/generation-evidence").as_posix()
    recorded = result["outputs"]["evidence"].get(relative)
    actual = sha256_file(path)
    print(
        f"trace_file={relative} actual={actual} recorded={recorded} "
        f"match={actual == recorded}"
    )

outer_types: Counter[str | None] = Counter()
payload_types: Counter[str | None] = Counter()
trace_line_count = 0
trace_parse_errors: list[str] = []
for path in trace_files:
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        trace_line_count += 1
        try:
            event = json.loads(line)
        except ValueError as error:
            trace_parse_errors.append(f"{path}:{line_number}:{error}")
            continue
        outer_types[event.get("type")] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_types[payload.get("type")] += 1
print(
    f"trace_lines={trace_line_count} parse_errors={trace_parse_errors} "
    f"outer_types={dict(outer_types)} payload_types={dict(payload_types)}"
)
print(
    f"invocation_status={invocation['status']} "
    f"invocation_exit={invocation['exit_code']} "
    f"result_marker={invocation['result_marker']}"
)
print(
    f"metrics_status={metrics['status']} metrics_exit={metrics['exit_code']} "
    f"usage_status={usage['status']} selected_event={usage['selected_event']}"
)

candidate_tree = pipeline_tree_sha256(Path("/candidate"))
trace_tree = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
print(
    f"candidate_pipeline_tree={candidate_tree} "
    f"result_workspace={result['outputs']['workspace_sha256']} "
    f"invocation_workspace={invocation['outputs']['workspace_sha256']} "
    f"match={candidate_tree == result['outputs']['workspace_sha256'] == invocation['outputs']['workspace_sha256']}"
)
print(
    f"trace_pipeline_tree={trace_tree} "
    f"usage_source_trace={usage['source_trace_sha256']} "
    f"match={trace_tree == usage['source_trace_sha256']}"
)
print(
    "launcher_recorded_candidate_tree_digest="
    f"{document['hashes']['candidate_tree_sha256']}"
)
print(
    "launcher_recorded_trace_tree_digest="
    f"{document['hashes']['generation_codex_trace_sha256']}"
)
