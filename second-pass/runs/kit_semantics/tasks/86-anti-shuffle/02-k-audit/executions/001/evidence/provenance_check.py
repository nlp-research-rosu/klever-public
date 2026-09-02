#!/usr/bin/env python3
"""Auditor-authored integrity checks for the pipeline-v3 mounts."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


sys.path.insert(0, "/opt/humaneval")
from tools.pipeline_contract import sha256_tree  # noqa: E402


AUDIT = json.loads(Path("/audit-input.json").read_text())


def sha(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require_regular(path: str | Path) -> None:
    mode = Path(path).lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")


def tree_manifest(root: Path):
    result = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            mode = child.stat(follow_symlinks=False).st_mode
            path = Path(child.path)
            rel = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[rel] = ("directory", stat.S_IMODE(mode), None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", stat.S_IMODE(mode), sha(path))
            else:
                raise AssertionError(f"linked/unsupported tree entry: {path}")
    return dict(sorted(result.items()))


def main() -> None:
    assert AUDIT["record_layout"] == "pipeline-v3"
    assert AUDIT["semantics_mode"] == "SUPPLIED_SEMANTICS"

    lock_path = Path(AUDIT["container_paths"]["audit_campaign_lock"])
    require_regular(lock_path)
    lock = json.loads(lock_path.read_text())
    assert lock == AUDIT["audit_campaign"]
    assert sha(lock_path) == AUDIT["hashes"]["audit_campaign_lock_sha256"]
    print("campaign_lock=PASS")

    required = {
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/runtime-metrics.json":
            "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log":
            "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    for path, key in required.items():
        require_regular(path)
        actual = sha(path)
        expected = AUDIT["hashes"][key]
        assert actual == expected, (path, actual, expected)
        print(f"record={path} sha256={actual} PASS")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert len(trace_files) == 1
    trace = trace_files[0]
    require_regular(trace)
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    rel = trace.relative_to("/generation-evidence").as_posix()
    expected_trace_file = invocation["outputs"]["evidence"][rel]
    assert sha(trace) == expected_trace_file
    event_count = 0
    with trace.open() as stream:
        for event_count, line in enumerate(stream, 1):
            parsed = json.loads(line)
            assert isinstance(parsed, dict)
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    trace_tree_hash = sha256_tree(Path("/generation-evidence/codex-trace"))
    assert trace_tree_hash == usage["source_trace_sha256"]
    print(
        f"trace=PASS files=1 events={event_count} "
        f"file_sha256={sha(trace)} tree_sha256={trace_tree_hash}"
    )

    for left, right, expected_key in (
        ("/candidate/prompt.py", "/reference/prompt.py",
         "trusted_prompt_sha256"),
        ("/candidate/py2mpy.py", "/reference/py2mpy.py",
         "trusted_translator_sha256"),
    ):
        require_regular(left)
        require_regular(right)
        assert Path(left).read_bytes() == Path(right).read_bytes()
        assert sha(right) == AUDIT["hashes"][expected_key]
        print(f"byte_identity={left}::{right} PASS")

    require_regular("/reference/canonical.py")
    assert sha("/reference/canonical.py") == AUDIT["hashes"]["canonical_sha256"]
    print("canonical_hash=PASS")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    assert tree_manifest(trusted_semantics) == tree_manifest(candidate_semantics)
    semantics_hash = sha256_tree(trusted_semantics)
    assert semantics_hash == AUDIT["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    task = json.loads(Path("/task.json").read_text())
    assert semantics_hash == task["inputs"]["reference_semantics_sha256"]
    print(
        "supplied_semantics=PASS "
        f"entries={len(tree_manifest(trusted_semantics))} "
        f"manifest_sha256={semantics_hash}"
    )

    candidate_hash = sha256_tree(Path("/candidate"))
    result = json.loads(Path("/generation-result.json").read_text())
    assert candidate_hash == result["outputs"]["workspace_sha256"]
    assert candidate_hash == invocation["outputs"]["workspace_sha256"]
    print(f"candidate_workspace=PASS manifest_sha256={candidate_hash}")
    print("overall=PASS")


if __name__ == "__main__":
    main()
