#!/usr/bin/env python3
"""Independent, read-only integrity and generation-record audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path
from typing import Any


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Reimplement the launcher's path/kind/size/content tree digest."""
    root_mode = root.lstat().st_mode
    if not stat.S_ISDIR(root_mode):
        raise ValueError(f"tree root is not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
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
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def content_tree_digest(root: Path) -> str:
    """Reimplement the launcher's compact path/kind/content tree digest."""
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def real_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return "unsupported"


def compare_trees(left: Path, right: Path) -> list[str]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        pending = [root]
        while pending:
            directory = pending.pop()
            for child in os.scandir(directory):
                path = Path(child.path)
                relative = path.relative_to(root).as_posix()
                kind = real_kind(path)
                if kind == "directory":
                    result[relative] = (kind, None)
                    pending.append(path)
                elif kind == "file":
                    result[relative] = (kind, sha256_file(path))
                else:
                    result[relative] = (kind, None)
        return result

    li = inventory(left)
    ri = inventory(right)
    issues: list[str] = []
    for path in sorted(set(li) | set(ri)):
        if path not in li:
            issues.append(f"missing candidate entry: {path}")
        elif path not in ri:
            issues.append(f"additional candidate entry: {path}")
        elif li[path] != ri[path]:
            issues.append(f"changed or mistyped candidate entry: {path}: {li[path]} != {ri[path]}")
    return issues


def extract_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(extract_text(item) for item in value)
    if isinstance(value, dict):
        for key in ("text", "message", "output", "arguments", "input"):
            if key in value:
                return extract_text(value[key])
    return ""


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    expected = audit["hashes"]
    issues: list[str] = []

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"problem_id={audit['problem_id']}")
    print(f"campaign_block_exact_match={audit['audit_campaign'] == lock}")
    if audit["audit_campaign"] != lock:
        issues.append("campaign block differs from campaign lock")

    required_files = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
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
        required_files.append(Path("/generation-evidence/usage.json"))
    required_dirs = [
        Path("/candidate"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
    ]
    for path in required_files:
        kind = real_kind(path) if path.exists() or path.is_symlink() else "missing"
        print(f"required {path}: {kind}")
        if kind != "file":
            issues.append(f"required file has kind {kind}: {path}")
    for path in required_dirs:
        kind = real_kind(path) if path.exists() or path.is_symlink() else "missing"
        print(f"required {path}: {kind}")
        if kind != "directory":
            issues.append(f"required directory has kind {kind}: {path}")

    file_hash_checks = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
    }
    for path_text, key in file_hash_checks.items():
        path = Path(path_text)
        if path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            wanted = expected.get(key)
            ok = actual == wanted
            print(f"hash {key}: actual={actual} expected={wanted} match={ok}")
            if not ok:
                issues.append(f"hash mismatch: {key}")

    # audit-input also carries launcher attestation digests computed by a
    # supervisor-side tree scheme whose implementation is not mounted.  Read
    # and report those values, then verify the mounted trees with two
    # independently available digest schemes plus direct recursive comparison.
    attested_tree_hashes = {
        "/candidate": "candidate_tree_sha256",
        "/candidate/reference-semantics": "candidate_reference_semantics_sha256",
        "/reference/reference-semantics": "trusted_reference_semantics_sha256",
        "/generation-evidence/codex-trace": "generation_codex_trace_sha256",
    }
    for path_text, key in attested_tree_hashes.items():
        path = Path(path_text)
        print(
            f"tree-attestation {key}: recorded={expected.get(key)} "
            f"independent_manifest_digest={sha256_tree(path)} "
            f"independent_content_digest={content_tree_digest(path)}"
        )

    manifest_tree_hash_checks = {
        "/candidate/reference-semantics": "trusted_reference_semantics_manifest_sha256",
    }
    for path_text, key in manifest_tree_hash_checks.items():
        path = Path(path_text)
        actual = sha256_tree(path)
        wanted = expected.get(key)
        ok = actual == wanted
        print(f"manifest-tree-hash {key}: actual={actual} expected={wanted} match={ok}")
        if not ok:
            issues.append(f"manifest tree hash mismatch: {key}")
    candidate_manifest = sha256_tree(Path("/candidate"))
    result_workspace = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )["outputs"]["workspace_sha256"]
    print(
        "manifest-tree-hash candidate workspace: "
        f"actual={candidate_manifest} expected={result_workspace} "
        f"match={candidate_manifest == result_workspace}"
    )
    if candidate_manifest != result_workspace:
        issues.append("candidate workspace differs from generation result workspace hash")
    trace_manifest = sha256_tree(Path("/generation-evidence/codex-trace"))
    usage_trace = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )["source_trace_sha256"]
    print(
        "manifest-tree-hash generation trace: "
        f"actual={trace_manifest} expected={usage_trace} "
        f"match={trace_manifest == usage_trace}"
    )
    if trace_manifest != usage_trace:
        issues.append("generation trace differs from usage source trace hash")

    byte_checks = [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "candidate prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "candidate translator"),
    ]
    for left, right, label in byte_checks:
        ok = left.read_bytes() == right.read_bytes()
        print(f"byte_identity {label}: {ok}")
        if not ok:
            issues.append(f"byte identity failed: {label}")

    tree_issues = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"reference_semantics_recursive_issue_count={len(tree_issues)}")
    for issue in tree_issues:
        print(f"TREE ISSUE: {issue}")
    issues.extend(tree_issues)

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*"))
    unsupported = [p for p in trace_files if real_kind(p) == "unsupported"]
    jsonl_files = [p for p in trace_files if p.is_file() and not p.is_symlink()]
    print(f"trace_file_count={len(jsonl_files)} unsupported_count={len(unsupported)}")
    if unsupported:
        issues.extend(f"unsupported trace entry: {p}" for p in unsupported)
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    response_item_types: Counter[str] = Counter()
    commands: list[str] = []
    final_messages: list[str] = []
    trace_lines = 0
    for path in jsonl_files:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                record = json.loads(line)
                event_types[str(record.get("type"))] += 1
                payload = record.get("payload", {})
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    if record.get("type") == "response_item":
                        response_item_types[str(payload.get("type"))] += 1
                        if payload.get("type") == "function_call":
                            commands.append(extract_text(payload))
                    if payload.get("type") == "agent_message":
                        message = extract_text(payload)
                        if "RESULT:" in message:
                            final_messages.append(message)
    print(f"trace_lines_read={trace_lines}")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_response_item_types={dict(sorted(response_item_types.items()))}")
    print(f"trace_function_call_records={len(commands)}")
    print(f"trace_final_message_count={len(final_messages)}")

    # Force a complete streaming read and classify the plain generation transcript.
    transcript = Path("/generation-evidence/codex-output.log")
    transcript_lines = 0
    transcript_bytes = 0
    noteworthy: Counter[str] = Counter()
    with transcript.open("rb") as stream:
        for raw_line in stream:
            transcript_lines += 1
            transcript_bytes += len(raw_line)
            line = raw_line.decode("utf-8", errors="replace")
            for token in ("kprove", "kompile", "krun", "#Top", "WarnStuckClaimState", "error:"):
                if token in line:
                    noteworthy[token] += 1
    print(f"codex_output_complete_read lines={transcript_lines} bytes={transcript_bytes}")
    print(f"codex_output_noteworthy_counts={dict(noteworthy)}")

    print(f"ISSUE_COUNT={len(issues)}")
    for issue in issues:
        print(f"ISSUE: {issue}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
