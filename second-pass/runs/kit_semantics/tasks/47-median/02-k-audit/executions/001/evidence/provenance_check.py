#!/usr/bin/env python3
"""Independent integrity checks for the mounted 47-median audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_file(path: Path) -> None:
    st = path.lstat()
    assert not path.is_symlink(), f"symlink where regular file required: {path}"
    assert path.is_file(), f"not a regular file: {path} ({st.st_mode:o})"
    with path.open("rb") as stream:
        stream.read(1)


def check_hash(label: str, path: Path, expected: str) -> None:
    require_file(path)
    actual = sha256(path)
    status = "OK" if actual == expected else "MISMATCH"
    print(f"{status} {label} {path} expected={expected} actual={actual}")
    assert actual == expected


def tree_manifest(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        st = path.lstat()
        if path.is_symlink():
            kind = "symlink"
            value = os.readlink(path)
        elif path.is_dir():
            kind = "directory"
            value = None
        elif path.is_file():
            kind = "file"
            value = sha256(path)
        else:
            kind = "other"
            value = None
        records.append(
            {"path": rel, "kind": kind, "mode": oct(st.st_mode & 0o777), "value": value}
        )
    return records


def digest_manifest(records: list[dict[str, Any]]) -> str:
    data = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    for path in (AUDIT, LOCK):
        require_file(path)
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert lock == audit["audit_campaign"], "campaign lock differs from audit block"
    print("OK campaign lock JSON exactly equals audit_campaign block")
    check_hash(
        "campaign-lock",
        LOCK,
        audit["hashes"]["audit_campaign_lock_sha256"],
    )

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
    ]
    for path in required:
        require_file(path)
    trace_root = Path("/generation-evidence/codex-trace")
    assert trace_root.is_dir() and not trace_root.is_symlink()
    trace_files = sorted(trace_root.rglob("*"))
    trace_files = [p for p in trace_files if p.is_file()]
    assert trace_files, "structured trace is empty"
    assert not any(p.is_symlink() for p in trace_root.rglob("*"))
    print(f"OK required pipeline-v3 records readable; trace_files={len(trace_files)}")

    direct = [
        ("run-manifest", Path("/run.json"), "run_manifest_sha256"),
        ("task-manifest", Path("/task.json"), "task_manifest_sha256"),
        ("stage1-result", Path("/generation-result.json"), "stage1_result_sha256"),
        (
            "stage1-invocation",
            Path("/generation-evidence/invocation.json"),
            "stage1_invocation_sha256",
        ),
        (
            "generation-metrics",
            Path("/generation-evidence/metrics.json"),
            "generation_metrics_sha256",
        ),
        (
            "generation-runtime-metrics",
            Path("/generation-evidence/runtime-metrics.json"),
            "generation_runtime_metrics_sha256",
        ),
        (
            "generation-usage",
            Path("/generation-evidence/usage.json"),
            "generation_usage_sha256",
        ),
        (
            "generation-last",
            Path("/generation-evidence/codex-last.txt"),
            "generation_codex_last_sha256",
        ),
        (
            "generation-output",
            Path("/generation-evidence/codex-output.log"),
            "generation_codex_output_sha256",
        ),
        (
            "generation-prompt",
            Path("/generation-evidence/prompt.txt"),
            "generation_prompt_sha256",
        ),
        ("canonical", Path("/reference/canonical.py"), "canonical_sha256"),
        ("trusted-prompt", Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        ("candidate-prompt", Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        ("trusted-translator", Path("/reference/py2mpy.py"), "trusted_translator_sha256"),
        ("candidate-translator", Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
    ]
    for label, path, hash_key in direct:
        check_hash(label, path, audit["hashes"][hash_key])

    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    for rel, expected in result["outputs"]["evidence"].items():
        check_hash(f"stage1-evidence:{rel}", Path("/generation-evidence") / rel, expected)

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("OK candidate prompt and translator are byte-identical to trusted mounts")

    trusted_sem = Path("/reference/reference-semantics")
    candidate_sem = Path("/candidate/reference-semantics")
    assert trusted_sem.is_dir() and not trusted_sem.is_symlink()
    assert candidate_sem.is_dir() and not candidate_sem.is_symlink()
    trusted_manifest = tree_manifest(trusted_sem)
    candidate_manifest = tree_manifest(candidate_sem)
    assert not any(rec["kind"] in {"symlink", "other"} for rec in trusted_manifest)
    assert not any(rec["kind"] in {"symlink", "other"} for rec in candidate_manifest)
    assert trusted_manifest == candidate_manifest, "reference-semantics trees differ"
    print(
        "OK candidate reference-semantics recursively identical "
        f"entries={len(trusted_manifest)} "
        f"independent_manifest_sha256={digest_manifest(trusted_manifest)}"
    )

    event_counts: dict[str, int] = {}
    session_ids: set[str] = set()
    first_timestamp = None
    last_timestamp = None
    trace_lines = 0
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                obj = json.loads(line)
                trace_lines += 1
                event_counts[obj.get("type", "<missing>")] = (
                    event_counts.get(obj.get("type", "<missing>"), 0) + 1
                )
                timestamp = obj.get("timestamp")
                first_timestamp = first_timestamp or timestamp
                last_timestamp = timestamp or last_timestamp
                payload = obj.get("payload", {})
                if isinstance(payload, dict):
                    sid = payload.get("session_id")
                    if isinstance(sid, str):
                        session_ids.add(sid)
    print(
        "OK structured trace parses "
        f"lines={trace_lines} first={first_timestamp} last={last_timestamp} "
        f"session_ids={sorted(session_ids)} event_counts={dict(sorted(event_counts.items()))}"
    )
    print("PROVENANCE_CHECK_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
