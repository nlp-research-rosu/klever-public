#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit record."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as inp:
        for block in iter(lambda: inp.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({mode:o})"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            digest = sha256(path) if entry_kind == "file" else None
            if entry_kind == "symlink":
                digest = os.readlink(path)
            result[rel] = (entry_kind, digest)
    return result


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the launcher/pipeline length-delimited tree hash."""
    entries = tree_entries(root)
    digest = hashlib.sha256()
    for relative, (entry_kind, _) in sorted(entries.items()):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(entry_kind.encode() + b"\0")
        if entry_kind == "file":
            path = root / relative
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as inp:
                for block in iter(lambda: inp.read(1024 * 1024), b""):
                    digest.update(block)
        elif entry_kind != "directory":
            raise ValueError(f"unsupported tree entry: {relative} ({entry_kind})")
    return digest.hexdigest()


def check_file(label: str, path: Path, expected: str | None) -> bool:
    if not path.exists() or kind(path) != "file":
        print(f"FAIL {label}: absent or not a regular file: {path}")
        return False
    actual = sha256(path)
    ok = expected is None or actual == expected
    print(
        f"{'PASS' if ok else 'FAIL'} {label}: kind=file sha256={actual}"
        + (f" expected={expected}" if expected else "")
    )
    return ok


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    failures = 0

    if audit["audit_campaign"] == lock:
        print("PASS campaign object exactly equals /audit-campaign-lock.json")
    else:
        print("FAIL campaign object differs from /audit-campaign-lock.json")
        failures += 1

    if not check_file(
        "campaign lock",
        LOCK,
        audit["hashes"]["audit_campaign_lock_sha256"],
    ):
        failures += 1
    if not check_file(
        "audit prompt",
        Path("/audit-prompt.md"),
        audit["audit_campaign"]["audit_prompt_sha256"],
    ):
        failures += 1

    expected_files = {
        "canonical": (
            Path(audit["container_paths"]["canonical"]),
            audit["hashes"]["canonical_sha256"],
        ),
        "trusted prompt": (
            Path(audit["container_paths"]["trusted_prompt"]),
            audit["hashes"]["trusted_prompt_sha256"],
        ),
        "candidate prompt": (
            Path(audit["container_paths"]["candidate"]) / "prompt.py",
            audit["hashes"]["candidate_prompt_sha256"],
        ),
        "trusted translator": (
            Path(audit["container_paths"]["translator"]),
            audit["hashes"]["trusted_translator_sha256"],
        ),
        "candidate translator": (
            Path(audit["container_paths"]["candidate"]) / "py2mpy.py",
            audit["hashes"]["candidate_translator_sha256"],
        ),
        "run manifest": (
            Path(audit["container_paths"]["run_manifest"]),
            audit["hashes"]["run_manifest_sha256"],
        ),
        "task manifest": (
            Path(audit["container_paths"]["task_manifest"]),
            audit["hashes"]["task_manifest_sha256"],
        ),
        "stage1 result": (
            Path(audit["container_paths"]["stage1_result"]),
            audit["hashes"]["stage1_result_sha256"],
        ),
        "invocation": (
            Path(audit["container_paths"]["generation_manifest"]),
            audit["hashes"]["stage1_invocation_sha256"],
        ),
        "generation metrics": (
            Path(audit["container_paths"]["generation_metrics"]),
            audit["hashes"]["generation_metrics_sha256"],
        ),
        "generation last": (
            Path(audit["container_paths"]["generation_last"]),
            audit["hashes"]["generation_codex_last_sha256"],
        ),
        "generation output": (
            Path(audit["container_paths"]["generation_output"]),
            audit["hashes"]["generation_codex_output_sha256"],
        ),
        "generation prompt": (
            Path(audit["container_paths"]["generation_root"]) / "prompt.txt",
            audit["hashes"]["generation_prompt_sha256"],
        ),
        "runtime metrics": (
            Path(audit["container_paths"]["generation_root"]) / "runtime-metrics.json",
            audit["hashes"]["generation_runtime_metrics_sha256"],
        ),
        "usage": (
            Path(audit["container_paths"]["generation_root"]) / "usage.json",
            audit["hashes"]["generation_usage_sha256"],
        ),
    }
    for label, (path, expected) in expected_files.items():
        if not check_file(label, path, expected):
            failures += 1

    candidate_ref = Path(audit["container_paths"]["candidate"]) / "reference-semantics"
    trusted_ref = Path("/reference/reference-semantics")
    if kind(candidate_ref) != "directory" or kind(trusted_ref) != "directory":
        print("FAIL supplied semantics trees are absent or not directories")
        failures += 1
    else:
        cand_entries = tree_entries(candidate_ref)
        trust_entries = tree_entries(trusted_ref)
        only_cand = sorted(cand_entries.keys() - trust_entries.keys())
        only_trust = sorted(trust_entries.keys() - cand_entries.keys())
        changed = sorted(
            rel
            for rel in cand_entries.keys() & trust_entries.keys()
            if cand_entries[rel] != trust_entries[rel]
        )
        if not only_cand and not only_trust and not changed:
            print(
                "PASS supplied semantics recursive identity: "
                f"{len(cand_entries)} entries, identical types and bytes"
            )
        else:
            print(f"FAIL candidate-only supplied semantics entries: {only_cand}")
            print(f"FAIL trusted-only supplied semantics entries: {only_trust}")
            print(f"FAIL mistyped/changed supplied semantics entries: {changed}")
            failures += 1
        symlinks = [
            rel for rel, (entry_kind, _) in cand_entries.items() if entry_kind == "symlink"
        ]
        if symlinks:
            print(f"FAIL candidate supplied semantics symlinks: {symlinks}")
            failures += 1
        else:
            print("PASS candidate supplied semantics contains no symlinks")

    for pair_label, left, right in [
        (
            "prompt bytes",
            Path("/candidate/prompt.py"),
            Path("/reference/prompt.py"),
        ),
        (
            "translator bytes",
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
        ),
    ]:
        same = left.read_bytes() == right.read_bytes()
        print(f"{'PASS' if same else 'FAIL'} {pair_label} identical")
        failures += not same

    trace_root = Path(audit["container_paths"]["generation_trace"])
    trace_entries = tree_entries(trace_root)
    trace_files = [
        trace_root / rel
        for rel, (entry_kind, _) in trace_entries.items()
        if entry_kind == "file"
    ]
    print(f"INFO structured trace regular files={len(trace_files)}")
    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    recorded_trace = {
        key.removeprefix("codex-trace/"): digest
        for key, digest in result["outputs"]["evidence"].items()
        if key.startswith("codex-trace/")
    }
    actual_trace = {
        path.relative_to(trace_root).as_posix(): sha256(path) for path in trace_files
    }
    if actual_trace == recorded_trace:
        print("PASS structured trace file set and hashes match generation-result.json")
    else:
        print(f"FAIL trace actual={actual_trace}")
        print(f"FAIL trace recorded={recorded_trace}")
        failures += 1
    if result["outputs"]["evidence"] == invocation["outputs"]["evidence"]:
        print("PASS result and invocation evidence hash maps agree")
    else:
        print("FAIL result and invocation evidence hash maps differ")
        failures += 1

    tree_checks = [
        (
            "candidate pipeline tree",
            Path(audit["container_paths"]["candidate"]),
            result["outputs"]["workspace_sha256"],
        ),
        (
            "trusted reference-semantics pipeline tree",
            trusted_ref,
            audit["manifest"]["inputs"]["reference_semantics_sha256"],
        ),
        (
            "candidate reference-semantics pipeline tree",
            candidate_ref,
            audit["manifest"]["inputs"]["reference_semantics_sha256"],
        ),
        (
            "structured trace pipeline tree",
            trace_root,
            json.loads(
                (Path(audit["container_paths"]["generation_root"]) / "usage.json").read_text()
            )["source_trace_sha256"],
        ),
    ]
    for label, path, expected in tree_checks:
        actual = pipeline_tree_sha256(path)
        ok = actual == expected
        print(
            f"{'PASS' if ok else 'FAIL'} {label}: "
            f"sha256={actual} expected={expected}"
        )
        failures += not ok

    event_counts: Counter[str] = Counter()
    line_count = 0
    parse_errors = 0
    session_ids: set[str] = set()
    first_timestamp: str | None = None
    last_timestamp: str | None = None
    for trace in trace_files:
        with trace.open() as inp:
            for line in inp:
                line_count += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    parse_errors += 1
                    continue
                event_counts[str(event.get("type", "<missing>"))] += 1
                timestamp = event.get("timestamp")
                if isinstance(timestamp, str):
                    first_timestamp = first_timestamp or timestamp
                    last_timestamp = timestamp
                payload = event.get("payload")
                if isinstance(payload, dict):
                    session_id = payload.get("id") if payload.get("type") == "session_meta" else None
                    if isinstance(session_id, str):
                        session_ids.add(session_id)
    print(
        "INFO structured trace fully parsed: "
        f"lines={line_count} parse_errors={parse_errors} "
        f"event_types={dict(sorted(event_counts.items()))} "
        f"session_ids={sorted(session_ids)} "
        f"first_timestamp={first_timestamp} last_timestamp={last_timestamp}"
    )
    if parse_errors:
        print("FAIL malformed JSONL trace records")
        failures += 1

    print(f"SUMMARY failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
