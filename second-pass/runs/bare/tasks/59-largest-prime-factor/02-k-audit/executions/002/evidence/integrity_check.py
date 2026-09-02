#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v2 tree digest used by stage-1 records."""
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
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
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")


def require_real_tree(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"not a real directory: {path}")
    for entry in path.rglob("*"):
        mode = entry.lstat().st_mode
        if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            raise AssertionError(f"linked/unsupported entry: {entry}")


audit_input_path = Path("/audit-input.json")
campaign_path = Path("/audit-campaign-lock.json")
audit_input = json.loads(audit_input_path.read_text())
campaign = json.loads(campaign_path.read_text())

assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit_input["audit_campaign"] == campaign
assert not Path("/reference/reference-semantics").exists()

required_files = [
    audit_input_path,
    campaign_path,
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
for path in required_files:
    require_regular(path)
for path in (
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
):
    require_real_tree(path)

recorded = audit_input["hashes"]
checks = {
    campaign_path: recorded["audit_campaign_lock_sha256"],
    Path("/candidate/prompt.py"): recorded["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): recorded["candidate_translator_sha256"],
    Path("/reference/canonical.py"): recorded["canonical_sha256"],
    Path("/reference/prompt.py"): recorded["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): recorded["trusted_translator_sha256"],
    Path("/run.json"): recorded["run_manifest_sha256"],
    Path("/task.json"): recorded["task_manifest_sha256"],
    Path("/generation-result.json"): recorded["stage1_result_sha256"],
    Path("/generation-evidence/invocation.json"): recorded[
        "stage1_invocation_sha256"
    ],
    Path("/generation-evidence/metrics.json"): recorded[
        "generation_metrics_sha256"
    ],
    Path("/generation-evidence/codex-last.txt"): recorded[
        "generation_codex_last_sha256"
    ],
    Path("/generation-evidence/codex-output.log"): recorded[
        "generation_codex_output_sha256"
    ],
    Path("/generation-evidence/prompt.txt"): recorded[
        "generation_prompt_sha256"
    ],
}
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    require_regular(usage)
    checks[usage] = recorded["generation_usage_sha256"]

for path, expected in checks.items():
    actual = sha256_file(path)
    print(f"FILE {path} {actual}")
    assert actual == expected, (path, actual, expected)

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()

generation_result = json.loads(Path("/generation-result.json").read_text())
evidence_hashes = generation_result["outputs"]["evidence"]
for relative, expected in sorted(evidence_hashes.items()):
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256_file(path)
    print(f"GENERATION {relative} {actual}")
    assert actual == expected, (path, actual, expected)

candidate_digest = pipeline_tree_sha256(Path("/candidate"))
expected_candidate_digest = generation_result["outputs"]["workspace_sha256"]
print(f"CANDIDATE_PIPELINE_TREE {candidate_digest}")
assert candidate_digest == expected_candidate_digest

trace_digest = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
print(f"TRACE_PIPELINE_TREE {trace_digest}")
if usage.exists():
    usage_record = json.loads(usage.read_text())
    assert trace_digest == usage_record["source_trace_sha256"]

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert trace_files
event_count = 0
events: list[dict] = []
for trace in trace_files:
    for line_number, line in enumerate(trace.open(), 1):
        event = json.loads(line)
        assert isinstance(event, dict)
        events.append(event)
        event_count += 1
if usage.exists():
    selected = usage_record["selected_event"]
    selected_path = Path("/generation-evidence/codex-trace") / selected[
        "relative_path"
    ]
    selected_event = json.loads(
        selected_path.read_text().splitlines()[selected["line_number"] - 1]
    )
    assert selected_event["payload"]["type"] == "token_count"

candidate_files = sorted(
    path for path in Path("/candidate").rglob("*") if path.is_file()
)
for path in candidate_files:
    print(
        f"CANDIDATE_FILE {path.relative_to('/candidate')} "
        f"{sha256_file(path)}"
    )
print(f"TRACE_JSON_EVENTS {event_count}")
print("INTEGRITY_OK")
