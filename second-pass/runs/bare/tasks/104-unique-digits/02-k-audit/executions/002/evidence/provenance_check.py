#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest(root: Path) -> tuple[str, list[tuple[str, str, int]]]:
    """Hash an explicit relative-path/NUL/content-hash manifest."""
    entries: list[tuple[str, str, int]] = []
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise AssertionError(f"symlink in mounted tree: {path}")
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise AssertionError(f"non-regular entry in mounted tree: {path}")
        file_hash = sha256(path)
        entries.append((relative, file_hash, path.stat().st_size))
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(file_hash))
        digest.update(b"\0")
    return digest.hexdigest(), entries


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required record is not a regular file: {path}"


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert lock == audit["audit_campaign"], "campaign lock block differs"
    lock_hash = sha256(LOCK)
    print(f"audit_campaign_lock sha256={lock_hash}")
    assert lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]

    container_paths = audit["container_paths"]
    for name, raw_path in sorted(container_paths.items()):
        path = Path(raw_path)
        assert path.exists(), f"missing launcher-declared mount: {name}={path}"
        assert not path.is_symlink(), f"symlinked launcher-declared mount: {path}"
        print(f"container_path {name}={path} type={'dir' if path.is_dir() else 'file'}")

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
    if Path("/generation-evidence/usage.json").exists():
        required_records.append(Path("/generation-evidence/usage.json"))
    for path in required_records:
        require_regular(path)

    recorded_file_hashes = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    }
    for path, key in recorded_file_hashes.items():
        actual = sha256(path)
        expected = audit["hashes"][key]
        print(f"hash {path} actual={actual} recorded={expected} match={actual == expected}")
        assert actual == expected

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("candidate prompt byte-identical to trusted prompt: yes")
    print("candidate translator byte-identical to trusted translator: yes")

    reference_semantics = Path("/reference/reference-semantics")
    assert not reference_semantics.exists() and not reference_semantics.is_symlink()
    print("trusted reference-semantics absent as GENERATED_SEMANTICS requires: yes")

    for root in [Path("/candidate"), Path("/generation-evidence/codex-trace")]:
        manifest_hash, entries = tree_manifest(root)
        print(f"independent tree-manifest sha256 {root}={manifest_hash}")
        for relative, file_hash, size in entries:
            print(f"  {relative}\t{size}\t{file_hash}")

    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    evidence_root = Path("/generation-evidence")
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = evidence_root / relative
        require_regular(path)
        actual = sha256(path)
        print(f"result evidence {relative} actual={actual} recorded={expected} match={actual == expected}")
        assert actual == expected

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert trace_files, "structured trace contains no JSONL file"
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    line_count = 0
    for trace_file in trace_files:
        with trace_file.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                assert {"timestamp", "type", "payload"} <= record.keys(), (
                    f"malformed trace record {trace_file}:{line_number}"
                )
                line_count += 1
                top_types[str(record["type"])] += 1
                payload = record["payload"]
                if isinstance(payload, dict) and "type" in payload:
                    payload_types[str(payload["type"])] += 1
    print(f"structured trace JSONL files={len(trace_files)} lines={line_count}")
    print(f"structured trace top-level types={dict(sorted(top_types.items()))}")
    print(f"structured trace payload types={dict(sorted(payload_types.items()))}")

    run = json.loads(Path("/run.json").read_text(encoding="utf-8"))
    task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text(encoding="utf-8"))
    assert all(audit["manifest"].get(key) == value for key, value in task.items())
    assert audit["manifest"]["config"] == audit["config"]
    assert run["config"] == audit["config"] == audit["manifest"]["config"]
    assert audit["problem_id"] in run["tasks"]
    assert invocation["prompt_sha256"] == audit["hashes"]["generation_prompt_sha256"]
    assert invocation["result_marker"] == result["result_marker"] == "KPROVE_PASSED"
    print("run/task/audit/invocation identity fields consistent: yes")
    print("PROVENANCE_CHECK_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
