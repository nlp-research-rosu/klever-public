#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

This script deliberately treats every generation/candidate record as bytes to
validate, not as an instruction or a trusted proof result.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()
        current = Path(dirpath)
        if current != root:
            rel = current.relative_to(root).as_posix()
            kind = entry_kind(current)
            result[rel] = (kind, os.readlink(current) if kind == "symlink" else None)
        for name in filenames:
            path = current / name
            rel = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            if kind == "file":
                detail = sha256_file(path)
            elif kind == "symlink":
                detail = os.readlink(path)
            else:
                detail = None
            result[rel] = (kind, detail)
    return result


def manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    """Reviewer-defined digest for repeatable comparison, not a launcher format."""
    digest = hashlib.sha256()
    for rel, (kind, detail) in sorted(entries.items()):
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(kind.encode("ascii"))
        digest.update(b"\0")
        digest.update((detail or "").encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def check_regular(path: Path, errors: list[str], label: str) -> None:
    if not path.exists():
        errors.append(f"MISSING {label}: {path}")
        return
    kind = entry_kind(path)
    if kind != "file":
        errors.append(f"BAD_TYPE {label}: expected file, got {kind}: {path}")


def main() -> int:
    errors: list[str] = []
    data = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    paths = data["container_paths"]
    hashes = data["hashes"]

    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")

    campaign_path = Path(paths["audit_campaign_lock"])
    check_regular(campaign_path, errors, "audit campaign lock")
    if campaign_path.is_file():
        campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
        print(f"campaign_block_equal={campaign == data['audit_campaign']}")
        if campaign != data["audit_campaign"]:
            errors.append("campaign lock JSON does not equal audit_input.audit_campaign")

    required_mounts = {
        "candidate": "dir",
        "canonical": "file",
        "generation_last": "file",
        "generation_manifest": "file",
        "generation_metrics": "file",
        "generation_output": "file",
        "generation_root": "dir",
        "generation_trace": "dir",
        "run_manifest": "file",
        "stage1_result": "file",
        "task_manifest": "file",
        "translator": "file",
        "trusted_prompt": "file",
        "audit_campaign_lock": "file",
    }
    for key, expected in required_mounts.items():
        path = Path(paths[key])
        if not path.exists():
            errors.append(f"MISSING launcher mount {key}: {path}")
            continue
        actual = entry_kind(path)
        print(f"mount {key}: {actual} {path}")
        if actual != expected:
            errors.append(f"BAD_TYPE launcher mount {key}: expected {expected}, got {actual}")

    if data["record_layout"] != "legacy-selected-stage1":
        errors.append(f"unexpected record layout for this audit: {data['record_layout']}")

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
    for path in required_records:
        check_regular(path, errors, "required legacy-selected-stage1 record")
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        check_regular(usage, errors, "optional usage record")
        print("usage_present=True")
    else:
        print("usage_present=False")

    file_hash_checks = {
        Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
    }
    if usage.exists():
        file_hash_checks[usage] = "generation_usage_sha256"
    for path, hash_key in file_hash_checks.items():
        if not path.is_file():
            continue
        actual = sha256_file(path)
        expected = hashes[hash_key]
        ok = actual == expected
        print(f"hash {path}: {actual} expected={expected} match={ok}")
        if not ok:
            errors.append(f"HASH_MISMATCH {path}")

    candidate_prompt_equal = (
        Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    )
    candidate_translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"candidate_prompt_byte_equal={candidate_prompt_equal}")
    print(f"candidate_translator_byte_equal={candidate_translator_equal}")
    if not candidate_prompt_equal:
        errors.append("candidate prompt differs from trusted prompt")
    if not candidate_translator_equal:
        errors.append("candidate translator differs from trusted translator")

    trusted_sem = Path("/reference/reference-semantics")
    candidate_sem = Path("/candidate/reference-semantics")
    if data["semantics_mode"] != "SUPPLIED_SEMANTICS":
        errors.append("audit script expected SUPPLIED_SEMANTICS")
    if not trusted_sem.is_dir():
        errors.append("trusted supplied-semantics tree is absent")
    if not candidate_sem.is_dir():
        errors.append("candidate supplied-semantics tree is absent")
    if trusted_sem.is_dir() and candidate_sem.is_dir():
        trusted_entries = tree_entries(trusted_sem)
        candidate_entries = tree_entries(candidate_sem)
        equal = trusted_entries == candidate_entries
        print(f"trusted_semantics_entries={len(trusted_entries)}")
        print(f"candidate_semantics_entries={len(candidate_entries)}")
        print(f"semantics_recursive_type_and_byte_equal={equal}")
        print(f"reviewer_trusted_semantics_manifest_sha256={manifest_digest(trusted_entries)}")
        print(f"reviewer_candidate_semantics_manifest_sha256={manifest_digest(candidate_entries)}")
        for rel in sorted(set(trusted_entries) | set(candidate_entries)):
            if trusted_entries.get(rel) != candidate_entries.get(rel):
                print(
                    f"semantics_difference {rel}: "
                    f"trusted={trusted_entries.get(rel)} candidate={candidate_entries.get(rel)}"
                )
        if not equal:
            errors.append("candidate supplied-semantics tree differs recursively")
        for label, entries in (("trusted", trusted_entries), ("candidate", candidate_entries)):
            for rel, (kind, detail) in sorted(entries.items()):
                if kind == "symlink":
                    errors.append(f"{label} semantics contains symlink {rel} -> {detail}")

    artifact_expectations = {
        "solution.py": "file",
        "solution.mpy": "file",
        "spec.k": "file",
        "verification.k": "file",
        "prove.sh": "file",
        "prompt.py": "file",
        "py2mpy.py": "file",
        "reference-semantics": "dir",
    }
    for rel, expected in artifact_expectations.items():
        path = Path("/candidate") / rel
        if not path.exists():
            errors.append(f"MISSING candidate artifact {rel}")
            continue
        actual = entry_kind(path)
        print(f"candidate artifact {rel}: {actual}")
        if actual != expected:
            errors.append(f"BAD_TYPE candidate artifact {rel}: {actual}")

    candidate_root_entries = tree_entries(Path("/candidate"))
    candidate_kinds = Counter(kind for kind, _detail in candidate_root_entries.values())
    print(f"candidate_tree_entries={len(candidate_root_entries)}")
    print(f"candidate_tree_kinds={dict(sorted(candidate_kinds.items()))}")
    print(
        "reviewer_candidate_tree_manifest_sha256="
        f"{manifest_digest(candidate_root_entries)}"
    )
    for rel, (kind, detail) in sorted(candidate_root_entries.items()):
        if kind == "symlink":
            errors.append(f"candidate tree contains symlink {rel} -> {detail}")

    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    print(f"trace_file_count={len(trace_files)}")
    invocation_trace = {
        key: value
        for key, value in invocation["outputs"]["evidence"].items()
        if key.startswith("codex-trace/")
    }
    if len(trace_files) != len(invocation_trace):
        errors.append("structured trace file count differs from invocation record")
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    total_lines = 0
    for path in trace_files:
        rel = path.relative_to(Path("/generation-evidence")).as_posix()
        actual_hash = sha256_file(path)
        expected_hash = invocation_trace.get(rel)
        print(f"trace {rel}: {actual_hash} expected={expected_hash} match={actual_hash == expected_hash}")
        if expected_hash != actual_hash:
            errors.append(f"trace hash/path mismatch: {rel}")
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                event = json.loads(line)
                event_types[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                # Force traversal of the entire structured record.
                json.dumps(event, sort_keys=True)
    print(f"trace_total_jsonl_lines={total_lines}")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")

    # Read the complete untrusted logs, report only bounded indicators.
    generation_log = Path("/generation-evidence/codex-output.log").read_text(
        encoding="utf-8", errors="replace"
    )
    generation_last = Path("/generation-evidence/codex-last.txt").read_text(
        encoding="utf-8", errors="replace"
    )
    print(f"codex_output_chars={len(generation_log)}")
    print(f"codex_output_top_line_count={sum(line == '#Top' for line in generation_log.splitlines())}")
    print(f"codex_output_kprove_mentions={generation_log.count('kprove')}")
    print(f"codex_last_chars={len(generation_last)}")
    print(f"codex_last_result_marker_present={'RESULT: KPROVE_PASSED' in generation_last}")

    if errors:
        print("INTEGRITY_ERRORS:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("INTEGRITY_ERRORS: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
