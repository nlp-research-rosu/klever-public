#!/usr/bin/env python3
"""Independent audit-mount inventory and declared-hash checker."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path, failures: list[str]) -> None:
    if path.is_symlink():
        failures.append(f"symlink forbidden: {path}")
    elif not path.is_file():
        failures.append(f"missing/not regular: {path}")
    elif not os.access(path, os.R_OK):
        failures.append(f"unreadable: {path}")
    else:
        print(f"REGULAR {sha256(path)} {path}")


def main() -> int:
    failures: list[str] = []
    require_regular(AUDIT_INPUT, failures)
    require_regular(LOCK, failures)
    if failures:
        print(*failures, sep="\n", file=sys.stderr)
        return 1

    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    if audit["audit_campaign"] != lock:
        failures.append("campaign block does not equal /audit-campaign-lock.json")
    actual_lock = sha256(LOCK)
    expected_lock = audit["hashes"]["audit_campaign_lock_sha256"]
    if actual_lock != expected_lock:
        failures.append(f"lock hash mismatch: {actual_lock} != {expected_lock}")
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_block_equal={audit['audit_campaign'] == lock}")
    print(f"campaign_hash_equal={actual_lock == expected_lock}")

    container_paths = audit["container_paths"]
    for key, raw_path in sorted(container_paths.items()):
        path = Path(raw_path)
        if key in {"candidate", "generation_root", "generation_trace"}:
            if path.is_symlink():
                failures.append(f"symlink forbidden: {key}={path}")
            elif not path.is_dir():
                failures.append(f"missing/not directory: {key}={path}")
            elif not os.access(path, os.R_OK | os.X_OK):
                failures.append(f"unreadable directory: {key}={path}")
            else:
                print(f"DIRECTORY {key} {path}")
        else:
            require_regular(path, failures)

    layout = audit["record_layout"]
    if layout == "legacy-selected-stage1":
        required = [
            Path("/run.json"),
            Path("/task.json"),
            Path("/generation-result.json"),
            Path("/generation-evidence/invocation.json"),
            Path("/generation-evidence/metrics.json"),
            Path("/generation-evidence/codex-last.txt"),
            Path("/generation-evidence/codex-output.log"),
            Path("/generation-evidence/prompt.txt"),
        ]
    else:
        failures.append(f"unexpected record layout for this checker: {layout}")
        required = []
    usage = Path("/generation-evidence/usage.json")
    if usage.exists() or usage.is_symlink():
        required.append(usage)
    for path in required:
        require_regular(path, failures)

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*")) if trace_root.is_dir() else []
    trace_regular = [path for path in trace_files if path.is_file() and not path.is_symlink()]
    trace_bad = [path for path in trace_files if path.is_symlink() or (not path.is_dir() and not path.is_file())]
    if not trace_regular:
        failures.append("structured trace contains no regular files")
    for path in trace_bad:
        failures.append(f"mistyped/symlinked trace entry: {path}")
    for path in trace_regular:
        print(f"TRACE {sha256(path)} {path}")

    hash_checks = {
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    }
    for path, key in hash_checks.items():
        expected = audit["hashes"].get(key)
        actual = sha256(path) if path.is_file() and not path.is_symlink() else None
        ok = actual == expected
        print(f"HASH_CHECK {key} ok={ok} actual={actual} expected={expected}")
        if not ok:
            failures.append(f"declared hash mismatch for {path} ({key})")

    for left, right, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]:
        equal = left.read_bytes() == right.read_bytes()
        print(f"BYTE_EQUAL {label} {equal}")
        if not equal:
            failures.append(f"candidate {label} differs from trusted mount")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_absent = not trusted_semantics.exists() and not trusted_semantics.is_symlink()
    candidate_absent = not candidate_semantics.exists() and not candidate_semantics.is_symlink()
    print(f"GENERATED_BOUNDARY trusted_reference_semantics_absent={trusted_absent}")
    print(f"GENERATED_BOUNDARY candidate_reference_semantics_absent={candidate_absent}")
    if audit["semantics_mode"] != "GENERATED_SEMANTICS":
        failures.append("rendered semantics mode is not GENERATED_SEMANTICS")
    if not trusted_absent:
        failures.append("trusted reference semantics exists in GENERATED_SEMANTICS mode")

    for root in [Path("/candidate"), Path("/reference"), Path("/generation-evidence")]:
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                failures.append(f"symlinked mounted artifact: {path}")

    print(f"failures={len(failures)}")
    if failures:
        print(*failures, sep="\n", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
