#!/usr/bin/env python3
"""Read-only integrity audit of launcher and generation records."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Mirror the installed pipeline_contract.sha256_tree encoding."""
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
                raise RuntimeError(f"unsupported or linked tree entry: {path}")
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
    mode = path.stat(follow_symlinks=False).st_mode
    if not stat.S_ISREG(mode) or path.is_symlink():
        raise RuntimeError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.stat(follow_symlinks=False).st_mode
    if not stat.S_ISDIR(mode) or path.is_symlink():
        raise RuntimeError(f"not a real directory: {path}")


def main() -> int:
    audit_input_path = Path("/audit-input.json")
    lock_path = Path("/audit-campaign-lock.json")
    audit_input = json.loads(audit_input_path.read_text())
    lock = json.loads(lock_path.read_text())
    print(f"record_layout={audit_input['record_layout']}")
    print(f"semantics_mode={audit_input['semantics_mode']}")
    print(f"campaign_object_equal={audit_input['audit_campaign'] == lock}")
    print(
        "campaign_lock_sha256="
        f"{file_sha256(lock_path)} "
        f"expected={audit_input['hashes']['audit_campaign_lock_sha256']}"
    )

    required_files = [
        audit_input_path,
        lock_path,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/semantic.k"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
    ]
    for path in required_files:
        require_regular(path)
    for path in (
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ):
        require_directory(path)
    print(f"required_regular_file_count={len(required_files)}")

    hash_checks = {
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
    failed_hashes = []
    for name, field in hash_checks.items():
        observed = file_sha256(Path(name))
        expected = audit_input["hashes"][field]
        ok = observed == expected
        print(f"hash_check={name} observed={observed} expected={expected} ok={ok}")
        if not ok:
            failed_hashes.append(name)

    candidate_tree_hash = pipeline_tree_sha256(Path("/candidate"))
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    print(f"candidate_pipeline_tree_sha256={candidate_tree_hash}")
    print(
        "candidate_pipeline_tree_expected="
        f"{invocation['retained_workspace_sha256']}"
    )

    trace_root = Path("/generation-evidence/codex-trace")
    trace_tree_hash = pipeline_tree_sha256(trace_root)
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    event_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    parsed_lines = 0
    for path in trace_files:
        require_regular(path)
        for line in path.open():
            event = json.loads(line)
            parsed_lines += 1
            event_counts[str(event.get("type"))] += 1
            payload_counts[str(event.get("payload", {}).get("type"))] += 1
    print(f"trace_pipeline_tree_sha256={trace_tree_hash}")
    print(f"trace_pipeline_tree_expected={usage['source_trace_sha256']}")
    print(f"trace_file_count={len(trace_files)}")
    print(f"trace_parsed_json_line_count={parsed_lines}")
    print(f"trace_event_counts={dict(sorted(event_counts.items()))}")
    print(f"trace_payload_counts={dict(sorted(payload_counts.items()))}")

    print(
        "candidate_prompt_byte_equal="
        f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
    )
    print(
        "candidate_translator_byte_equal="
        f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
    )
    print(
        "reference_semantics_absent="
        f"{not Path('/reference/reference-semantics').exists()}"
    )

    ok = (
        not failed_hashes
        and audit_input["audit_campaign"] == lock
        and candidate_tree_hash == invocation["retained_workspace_sha256"]
        and trace_tree_hash == usage["source_trace_sha256"]
        and not Path("/reference/reference-semantics").exists()
    )
    print(f"RESULT={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
