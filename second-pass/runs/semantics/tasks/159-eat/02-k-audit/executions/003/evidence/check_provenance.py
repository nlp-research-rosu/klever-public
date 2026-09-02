#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise AssertionError(f"required regular file has wrong type: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def tree_manifest(root: Path) -> tuple[dict[str, tuple[str, int, str]], str]:
    records: dict[str, tuple[str, int, str]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            kind, digest = "symlink", os.readlink(path)
        elif stat.S_ISDIR(info.st_mode):
            kind, digest = "directory", ""
        elif stat.S_ISREG(info.st_mode):
            kind, digest = "file", sha256(path)
        else:
            kind, digest = "other", ""
        records[relative] = (kind, info.st_size, digest)
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return records, hashlib.sha256(encoded).hexdigest()


def check_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256(path)
    if actual != expected:
        raise AssertionError(
            f"{label} hash mismatch: expected={expected} actual={actual}"
        )
    print(f"hash_ok {label} {actual} {path}")


def main() -> int:
    require_regular(AUDIT)
    require_regular(LOCK)
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    if audit["record_layout"] != "legacy-selected-stage1":
        raise AssertionError(f"unexpected record layout {audit['record_layout']}")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise AssertionError(f"unexpected semantics mode {audit['semantics_mode']}")
    if lock != audit["audit_campaign"]:
        raise AssertionError("campaign lock content differs from audit campaign block")
    print("record_layout=legacy-selected-stage1")
    print("semantics_mode=SUPPLIED_SEMANTICS")
    print("campaign_block_match=true")

    hashes = audit["hashes"]
    checks = [
        ("audit_campaign_lock", LOCK, hashes["audit_campaign_lock_sha256"]),
        ("canonical", Path("/reference/canonical.py"), hashes["canonical_sha256"]),
        ("trusted_prompt", Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"]),
        ("trusted_translator", Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"]),
        ("candidate_prompt", Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"]),
        ("candidate_translator", Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"]),
        ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        ("stage1_result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
        ("invocation", Path("/generation-evidence/invocation.json"), hashes["stage1_invocation_sha256"]),
        ("metrics", Path("/generation-evidence/metrics.json"), hashes["generation_metrics_sha256"]),
        ("codex_last", Path("/generation-evidence/codex-last.txt"), hashes["generation_codex_last_sha256"]),
        ("codex_output", Path("/generation-evidence/codex-output.log"), hashes["generation_codex_output_sha256"]),
        ("generation_prompt", Path("/generation-evidence/prompt.txt"), hashes["generation_prompt_sha256"]),
        ("usage", Path("/generation-evidence/usage.json"), hashes["generation_usage_sha256"]),
    ]
    for label, path, expected in checks:
        check_hash(label, path, expected)

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
    for path in required:
        require_regular(path)
    print(f"required_layout_records={len(required)} all_regular_and_readable=true")

    trusted, trusted_digest = tree_manifest(Path("/reference/reference-semantics"))
    candidate, candidate_digest = tree_manifest(Path("/candidate/reference-semantics"))
    if trusted != candidate:
        missing = sorted(set(trusted) - set(candidate))
        extra = sorted(set(candidate) - set(trusted))
        changed = sorted(
            key for key in set(trusted) & set(candidate) if trusted[key] != candidate[key]
        )
        raise AssertionError(
            f"semantics tree differs missing={missing} extra={extra} changed={changed}"
        )
    if any(record[0] == "symlink" for record in trusted.values()):
        raise AssertionError("trusted semantics contains symlink")
    if any(record[0] == "symlink" for record in candidate.values()):
        raise AssertionError("candidate semantics contains symlink")
    print(f"semantics_entries={len(trusted)} recursive_exact_match=true symlinks=0")
    print(f"independent_semantics_manifest_sha256={trusted_digest}")
    print(f"candidate_semantics_manifest_sha256={candidate_digest}")

    candidate_tree, candidate_tree_digest = tree_manifest(Path("/candidate"))
    print(f"candidate_entries={len(candidate_tree)}")
    print(f"independent_candidate_manifest_sha256={candidate_tree_digest}")

    generation_result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    trace_outputs = {
        key: value
        for key, value in generation_result["outputs"]["evidence"].items()
        if key.startswith("codex-trace/")
    }
    actual_trace_files = sorted(
        path for path in Path("/generation-evidence/codex-trace").rglob("*") if path.is_file()
    )
    if len(trace_outputs) != len(actual_trace_files):
        raise AssertionError("structured trace file count mismatch")
    event_types = Counter()
    response_types = Counter()
    line_count = 0
    for relative, expected in trace_outputs.items():
        path = Path("/generation-evidence") / relative
        check_hash("structured_trace", path, expected)
        with path.open(encoding="utf-8") as stream:
            for line_count, line in enumerate(stream, 1):
                event = json.loads(line)
                event_types[event.get("type")] += 1
                if event.get("type") == "response_item":
                    response_types[event.get("payload", {}).get("type")] += 1
    Path("/generation-evidence/codex-output.log").read_text(encoding="utf-8")
    print(f"trace_json_lines={line_count} all_json_valid=true")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_response_types={dict(sorted(response_types.items()))}")
    print("codex_output_utf8_read_complete=true")

    proof_artifacts = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
    ]
    for path in proof_artifacts:
        require_regular(path)
    print("required_candidate_proof_artifacts=5 all_regular_and_readable=true")
    print("integrity_result=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
