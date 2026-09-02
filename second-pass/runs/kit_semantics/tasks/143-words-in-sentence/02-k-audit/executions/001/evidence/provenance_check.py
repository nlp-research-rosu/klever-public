#!/usr/bin/env python3
"""Independent, read-only validation of the audit launcher inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_readable(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and os.access(path, os.R_OK)


def tree_manifest(root: Path) -> tuple[list[tuple[str, str]], str]:
    entries: list[tuple[str, str]] = []
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries.append((rel, "SYMLINK"))
        elif stat.S_ISREG(mode):
            file_hash = sha256_file(path)
            entries.append((rel, file_hash))
        elif stat.S_ISDIR(mode):
            entries.append((rel + "/", "DIRECTORY"))
        else:
            entries.append((rel, "OTHER"))
    for rel, kind_hash in entries:
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(kind_hash.encode("ascii"))
        digest.update(b"\0")
    return entries, digest.hexdigest()


def launcher_tree_sha256(root: Path) -> str:
    """Recompute the pipeline-v3 length-framed tree digest independently."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((relative, "file", path))
        else:
            raise ValueError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.lstat().st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def check_hash(label: str, path: Path, expected: str) -> bool:
    actual = sha256_file(path)
    ok = actual == expected
    print(f"HASH {label} {'PASS' if ok else 'FAIL'} expected={expected} actual={actual} path={path}")
    return ok


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    if lock != audit["audit_campaign"]:
        failures.append("campaign JSON object mismatch")
    print(f"CAMPAIGN_OBJECT {'PASS' if not failures else 'FAIL'}")

    if not check_hash(
        "audit_campaign_lock",
        LOCK,
        audit["hashes"]["audit_campaign_lock_sha256"],
    ):
        failures.append("campaign lock hash mismatch")

    required_regular = {
        "run_manifest": Path("/run.json"),
        "task_manifest": Path("/task.json"),
        "stage1_result": Path("/generation-result.json"),
        "stage1_invocation": Path("/generation-evidence/invocation.json"),
        "generation_metrics": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage": Path("/generation-evidence/usage.json"),
        "generation_last": Path("/generation-evidence/codex-last.txt"),
        "generation_output": Path("/generation-evidence/codex-output.log"),
        "generation_prompt": Path("/generation-evidence/prompt.txt"),
        "canonical": Path("/reference/canonical.py"),
        "trusted_prompt": Path("/reference/prompt.py"),
        "trusted_translator": Path("/reference/py2mpy.py"),
    }
    hash_keys = {
        "run_manifest": "run_manifest_sha256",
        "task_manifest": "task_manifest_sha256",
        "stage1_result": "stage1_result_sha256",
        "stage1_invocation": "stage1_invocation_sha256",
        "generation_metrics": "generation_metrics_sha256",
        "generation_runtime_metrics": "generation_runtime_metrics_sha256",
        "generation_usage": "generation_usage_sha256",
        "generation_last": "generation_codex_last_sha256",
        "generation_output": "generation_codex_output_sha256",
        "generation_prompt": "generation_prompt_sha256",
        "canonical": "canonical_sha256",
        "trusted_prompt": "trusted_prompt_sha256",
        "trusted_translator": "trusted_translator_sha256",
    }
    for label, path in required_regular.items():
        ok_type = regular_readable(path) and not path.is_symlink()
        print(f"TYPE {label} {'PASS' if ok_type else 'FAIL'} regular-readable-no-symlink path={path}")
        if not ok_type:
            failures.append(f"bad required record type: {label}")
            continue
        if not check_hash(label, path, audit["hashes"][hash_keys[label]]):
            failures.append(f"hash mismatch: {label}")
        # Decode and fully scan every text record, including the large output log.
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
            print(f"SCAN {label} PASS bytes={len(data)} lines={len(text.splitlines())} utf8=true")
        except UnicodeDecodeError:
            print(f"SCAN {label} FAIL bytes={len(data)} utf8=false")
            failures.append(f"non-UTF8 required text record: {label}")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*"))
    trace_regular = [p for p in trace_files if p.is_file() and not p.is_symlink()]
    bad_trace_entries = [p for p in trace_files if p.is_symlink() or (not p.is_dir() and not p.is_file())]
    if len(trace_regular) != 1 or bad_trace_entries:
        failures.append("structured trace inventory mismatch")
    trace_manifest = json.loads(Path("/generation-result.json").read_text())["outputs"]["evidence"]
    for path in trace_regular:
        rel = path.relative_to(Path("/generation-evidence")).as_posix()
        expected = trace_manifest.get(rel)
        actual = sha256_file(path)
        print(f"TRACE_HASH {'PASS' if expected == actual else 'FAIL'} rel={rel} expected={expected} actual={actual}")
        if expected != actual:
            failures.append(f"trace hash mismatch: {rel}")
        count = 0
        type_counts: dict[str, int] = {}
        with path.open(encoding="utf-8") as stream:
            for line_no, line in enumerate(stream, 1):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as err:
                    failures.append(f"invalid JSONL {rel}:{line_no}: {err}")
                    continue
                count += 1
                rec_type = str(record.get("type", "<missing>"))
                type_counts[rec_type] = type_counts.get(rec_type, 0) + 1
        print(f"TRACE_SCAN records={count} types={json.dumps(type_counts, sort_keys=True)}")

    for label, candidate_path, trusted_path, recorded_hash in (
        (
            "candidate_prompt",
            Path("/candidate/prompt.py"),
            Path("/reference/prompt.py"),
            audit["hashes"]["candidate_prompt_sha256"],
        ),
        (
            "candidate_translator",
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
            audit["hashes"]["candidate_translator_sha256"],
        ),
    ):
        ok = (
            regular_readable(candidate_path)
            and not candidate_path.is_symlink()
            and candidate_path.read_bytes() == trusted_path.read_bytes()
            and sha256_file(candidate_path) == recorded_hash
        )
        print(f"TRUSTED_COPY {label} {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"candidate trusted copy mismatch: {label}")

    candidate_sem = Path("/candidate/reference-semantics")
    trusted_sem = Path("/reference/reference-semantics")
    candidate_entries, candidate_tree_hash = tree_manifest(candidate_sem)
    trusted_entries, trusted_tree_hash = tree_manifest(trusted_sem)
    sem_ok = candidate_entries == trusted_entries
    candidate_pipeline_sem_hash = launcher_tree_sha256(candidate_sem)
    trusted_pipeline_sem_hash = launcher_tree_sha256(trusted_sem)
    sem_hash_ok = (
        candidate_pipeline_sem_hash
        == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
        and trusted_pipeline_sem_hash
        == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    )
    print(
        "SEMANTICS_TREE "
        f"{'PASS' if sem_ok and sem_hash_ok else 'FAIL'} entries={len(candidate_entries)} "
        f"auditor_candidate_hash={candidate_tree_hash} auditor_trusted_hash={trusted_tree_hash} "
        f"pipeline_candidate_hash={candidate_pipeline_sem_hash} "
        f"pipeline_trusted_hash={trusted_pipeline_sem_hash}"
    )
    for rel, kind_hash in candidate_entries:
        print(f"SEMANTICS_ENTRY {rel} {kind_hash}")
    if not sem_ok or not sem_hash_ok:
        failures.append("candidate supplied semantics differs from trusted tree")

    candidate_entries_all, candidate_tree_hash_all = tree_manifest(Path("/candidate"))
    candidate_pipeline_hash_all = launcher_tree_sha256(Path("/candidate"))
    candidate_symlinks = [rel for rel, kind_hash in candidate_entries_all if kind_hash == "SYMLINK"]
    candidate_other = [rel for rel, kind_hash in candidate_entries_all if kind_hash == "OTHER"]
    print(
        "CANDIDATE_TREE_SCAN "
        f"entries={len(candidate_entries_all)} auditor_sha256={candidate_tree_hash_all} "
        f"pipeline_sha256={candidate_pipeline_hash_all} "
        f"symlinks={len(candidate_symlinks)} unsupported={len(candidate_other)}"
    )
    generation_workspace_hash = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )["outputs"]["workspace_sha256"]
    if (
        candidate_symlinks
        or candidate_other
        or candidate_pipeline_hash_all != generation_workspace_hash
    ):
        failures.append("candidate tree type or recorded hash mismatch")

    required_candidate = (
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    )
    for name in required_candidate:
        path = Path("/candidate") / name
        ok = regular_readable(path) and not path.is_symlink()
        print(f"CANDIDATE_ARTIFACT {name} {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"missing or mistyped candidate artifact: {name}")

    print(f"RECORD_LAYOUT {audit.get('record_layout')}")
    print(f"SEMANTICS_MODE {audit.get('semantics_mode')}")
    print(f"PROVENANCE_FAILURES {len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
