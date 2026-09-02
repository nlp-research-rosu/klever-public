#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def walk_tree(root: Path) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    for current, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        dirnames.sort()
        filenames.sort()
        current_path = Path(current)
        for name in dirnames + filenames:
            path = current_path / name
            mode = path.lstat().st_mode
            rel = path.relative_to(root).as_posix()
            if stat.S_ISLNK(mode):
                entries.append((rel, "symlink", os.readlink(path)))
            elif stat.S_ISDIR(mode):
                entries.append((rel, "dir", ""))
            elif stat.S_ISREG(mode):
                entries.append((rel, "file", digest(path)))
            else:
                entries.append((rel, "other", oct(mode)))
    return entries


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the pipeline-v3 length-delimited tree hash."""
    root = root.resolve(strict=True)
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    h = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
        h.update(kind.encode() + bytes([0]))
        if kind == "file":
            h.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    h.update(chunk)
    return h.hexdigest()


def main() -> int:
    record = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    errors: list[str] = []

    print(f"record_layout={record.get('record_layout')}")
    print(f"semantics_mode={record.get('semantics_mode')}")
    print(f"audit_campaign_lock_sha256={digest(LOCK)}")
    print(f"expected_audit_campaign_lock_sha256={record['hashes']['audit_campaign_lock_sha256']}")
    if digest(LOCK) != record["hashes"]["audit_campaign_lock_sha256"]:
        errors.append("campaign lock digest mismatch")
    if lock != record["audit_campaign"]:
        errors.append("campaign lock JSON does not equal audit_campaign block")

    required = {
        "audit-input": AUDIT_INPUT,
        "audit-campaign-lock": LOCK,
        "run": Path("/run.json"),
        "task": Path("/task.json"),
        "generation-result": Path("/generation-result.json"),
        "invocation": Path("/generation-evidence/invocation.json"),
        "metrics": Path("/generation-evidence/metrics.json"),
        "runtime-metrics": Path("/generation-evidence/runtime-metrics.json"),
        "usage": Path("/generation-evidence/usage.json"),
        "codex-last": Path("/generation-evidence/codex-last.txt"),
        "codex-output": Path("/generation-evidence/codex-output.log"),
        "generation-prompt": Path("/generation-evidence/prompt.txt"),
        "trace": Path("/generation-evidence/codex-trace"),
        "candidate": Path("/candidate"),
        "canonical": Path("/reference/canonical.py"),
        "trusted-prompt": Path("/reference/prompt.py"),
        "translator": Path("/reference/py2mpy.py"),
        "trusted-semantics": Path("/reference/reference-semantics"),
    }
    for label, path in required.items():
        kind = "missing"
        if path.exists():
            mode = path.lstat().st_mode
            kind = (
                "symlink"
                if stat.S_ISLNK(mode)
                else "dir"
                if stat.S_ISDIR(mode)
                else "file"
                if stat.S_ISREG(mode)
                else "other"
            )
        print(f"required[{label}]={kind}:{path}")
        if not path.exists() or path.is_symlink():
            errors.append(f"bad required mount: {label} ({kind})")

    candidate_proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for name in candidate_proof_artifacts:
        path = Path("/candidate") / name
        good = path.exists() and path.is_file() and not path.is_symlink()
        print(f"candidate_proof_artifact[{name}]=regular={good}")
        if not good:
            errors.append(f"candidate proof artifact missing/mistyped/symlinked: {name}")

    direct_hashes = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
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
    for raw_path, key in direct_hashes.items():
        path = Path(raw_path)
        actual = digest(path)
        expected = record["hashes"][key]
        print(f"sha256[{raw_path}]={actual} expected={expected} match={actual == expected}")
        if actual != expected:
            errors.append(f"digest mismatch: {raw_path}")

    manifest = json.loads(Path("/generation-evidence/invocation.json").read_text())
    for rel, expected in sorted(manifest["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / rel
        actual = digest(path)
        print(f"invocation-evidence[{rel}]={actual} expected={expected} match={actual == expected}")
        if actual != expected:
            errors.append(f"invocation evidence digest mismatch: {rel}")

    result = json.loads(Path("/generation-result.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    pipeline_tree_checks = [
        (
            Path("/candidate"),
            result["outputs"]["workspace_sha256"],
            "generation-result workspace",
        ),
        (
            Path("/reference/reference-semantics"),
            record["hashes"]["trusted_reference_semantics_manifest_sha256"],
            "trusted reference semantics manifest",
        ),
        (
            Path("/candidate/reference-semantics"),
            record["manifest"]["inputs"]["reference_semantics_sha256"],
            "candidate reference semantics manifest",
        ),
        (
            Path("/generation-evidence/codex-trace"),
            usage["source_trace_sha256"],
            "usage source trace",
        ),
    ]
    for path, expected, label in pipeline_tree_checks:
        actual = pipeline_tree_digest(path)
        print(f"pipeline_tree_sha256[{path}]={actual} expected={expected} label={label} match={actual == expected}")
        if actual != expected:
            errors.append(f"pipeline tree digest mismatch: {path}")

    trusted_semantics = walk_tree(Path("/reference/reference-semantics"))
    candidate_semantics = walk_tree(Path("/candidate/reference-semantics"))
    print(f"trusted_semantics_entries={len(trusted_semantics)}")
    print(f"candidate_semantics_entries={len(candidate_semantics)}")
    print(f"semantics_trees_identical={trusted_semantics == candidate_semantics}")
    print(f"trusted_semantics_types={dict(Counter(kind for _, kind, _ in trusted_semantics))}")
    print(f"candidate_semantics_types={dict(Counter(kind for _, kind, _ in candidate_semantics))}")
    if trusted_semantics != candidate_semantics:
        errors.append("candidate and trusted semantics trees differ")
    if any(kind == "symlink" for _, kind, _ in candidate_semantics):
        errors.append("candidate semantics contains symlinks")

    prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not prompt_equal:
        errors.append("candidate prompt differs from trusted prompt")
    if not translator_equal:
        errors.append("candidate translator differs from trusted translator")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    trace_event_counts: Counter[str] = Counter()
    trace_payload_counts: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        if path.is_symlink():
            errors.append(f"trace symlink: {path}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as err:
                    errors.append(f"invalid JSONL {path}:{line_number}: {err}")
                    continue
                trace_event_counts[event.get("type", "<missing>")] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    trace_payload_counts[payload.get("type", "<missing>")] += 1
    print(f"trace_files={len(trace_files)}")
    print(f"trace_lines_parsed={trace_lines}")
    print(f"trace_event_types={dict(sorted(trace_event_counts.items()))}")
    print(f"trace_payload_types={dict(sorted(trace_payload_counts.items()))}")

    # Force complete reads and report simple shape for the untrusted text records.
    for path in [
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]:
        data = path.read_bytes()
        print(f"complete_read[{path}] bytes={len(data)} lines={data.count(bytes([10]))}")

    print(f"errors={len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
