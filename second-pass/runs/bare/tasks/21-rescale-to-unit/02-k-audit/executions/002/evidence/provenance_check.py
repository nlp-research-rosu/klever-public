#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE_ROOT = Path("/generation-evidence/codex-trace")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a regular file: {path}")


def main() -> int:
    document = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    assert document["record_layout"] == "legacy-selected-stage1"
    assert document["semantics_mode"] == "GENERATED_SEMANTICS"
    assert document["audit_campaign"] == lock
    assert sha256_file(LOCK) == document["hashes"]["audit_campaign_lock_sha256"]

    required = {
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
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
    for name, key in required.items():
        path = Path(name)
        require_regular(path)
        actual = sha256_file(path)
        expected = document["hashes"][key]
        print(f"FILE {name} sha256={actual} recorded={expected} match={actual == expected}")
        assert actual == expected

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    assert not os.path.lexists("/reference/reference-semantics")

    for root in (Path("/candidate"), Path("/reference"), Path("/generation-evidence")):
        linked = [path for path in root.rglob("*") if path.is_symlink()]
        print(f"SYMLINKS {root}: {linked}")
        assert not linked

    result = json.loads(Path("/generation-result.json").read_text())
    trace_outputs = {
        key: value
        for key, value in result["outputs"]["evidence"].items()
        if key.startswith("codex-trace/")
    }
    observed_trace = {}
    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    malformed = 0
    total_lines = 0
    for path in sorted(TRACE_ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(Path("/generation-evidence")).as_posix()
        observed_trace[rel] = sha256_file(path)
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                total_lines += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                event_types[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
    print(f"TRACE recorded={trace_outputs}")
    print(f"TRACE observed={observed_trace}")
    print(f"TRACE lines={total_lines} malformed={malformed}")
    print(f"TRACE event_types={dict(event_types)}")
    print(f"TRACE payload_types={dict(payload_types)}")
    assert observed_trace == trace_outputs
    assert malformed == 0

    sys.path.insert(0, "/opt/humaneval")
    from tools.pipeline_contract import sha256_tree

    candidate_pipeline_hash = sha256_tree(Path("/candidate"))
    trace_pipeline_hash = sha256_tree(TRACE_ROOT)
    print(f"CANDIDATE pipeline_tree_sha256={candidate_pipeline_hash}")
    print(
        "CANDIDATE stage1_retained_sha256="
        f"{json.loads(Path('/generation-evidence/invocation.json').read_text())['retained_workspace_sha256']}"
    )
    print(f"TRACE pipeline_tree_sha256={trace_pipeline_hash}")
    print(
        "TRACE usage_source_sha256="
        f"{json.loads(Path('/generation-evidence/usage.json').read_text())['source_trace_sha256']}"
    )
    assert (
        candidate_pipeline_hash
        == json.loads(Path("/generation-evidence/invocation.json").read_text())[
            "retained_workspace_sha256"
        ]
    )
    assert (
        trace_pipeline_hash
        == json.loads(Path("/generation-evidence/usage.json").read_text())[
            "source_trace_sha256"
        ]
    )
    print("PROVENANCE_CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
