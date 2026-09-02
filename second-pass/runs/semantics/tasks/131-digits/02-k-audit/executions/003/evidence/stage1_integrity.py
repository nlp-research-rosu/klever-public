#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_regular(path: Path, label: str) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        raise AssertionError(f"{label}: absent or unreadable: {err}") from err
    assert stat.S_ISREG(mode), f"{label}: expected regular file, mode={oct(mode)}"
    print(f"OK regular {label}: {path}")


def require_directory(path: Path, label: str) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        raise AssertionError(f"{label}: absent or unreadable: {err}") from err
    assert stat.S_ISDIR(mode), f"{label}: expected directory, mode={oct(mode)}"
    print(f"OK directory {label}: {path}")


def compare_regular_files(left: Path, right: Path, label: str) -> None:
    require_regular(left, f"{label} left")
    require_regular(right, f"{label} right")
    left_hash, right_hash = digest(left), digest(right)
    assert left_hash == right_hash, (
        f"{label}: byte mismatch: left={left_hash} right={right_hash}"
    )
    print(f"OK byte-identical {label}: sha256={left_hash}")


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    require_directory(root, f"tree {root}")
    entries: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries[rel] = ("symlink", os.readlink(path))
        elif stat.S_ISDIR(mode):
            entries[rel] = ("directory", None)
        elif stat.S_ISREG(mode):
            entries[rel] = ("regular", digest(path))
        else:
            entries[rel] = (f"other:{oct(mode)}", None)
    return entries


def transparent_tree_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    """Reviewer-defined digest over relative path, type, and content/link hash."""
    h = hashlib.sha256()
    for rel, (kind, value) in sorted(entries.items()):
        h.update(rel.encode())
        h.update(b"\0")
        h.update(kind.encode())
        h.update(b"\0")
        if value is not None:
            h.update(value.encode())
        h.update(b"\n")
    return h.hexdigest()


def check_hash(path: Path, expected: str, label: str) -> None:
    require_regular(path, label)
    actual = digest(path)
    assert actual == expected, f"{label}: expected {expected}, got {actual}"
    print(f"OK recorded hash {label}: {actual}")


def main() -> None:
    require_regular(AUDIT_INPUT, "audit input")
    require_regular(LOCK, "campaign lock")
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    assert audit["audit_campaign"] == lock, "campaign block differs from lock JSON"
    print("OK campaign block exactly matches campaign lock JSON")
    check_hash(
        LOCK,
        audit["hashes"]["audit_campaign_lock_sha256"],
        "campaign lock",
    )

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    print("OK layout=legacy-selected-stage1 semantics=SUPPLIED_SEMANTICS")

    paths = {name: Path(value) for name, value in audit["container_paths"].items()}
    required_path_keys = [
        "audit_campaign_lock",
        "candidate",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "generation_root",
        "generation_trace",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    ]
    for key in required_path_keys:
        path = paths[key]
        if key in {"candidate", "generation_root", "generation_trace"}:
            require_directory(path, f"container_paths.{key}")
        else:
            require_regular(path, f"container_paths.{key}")

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
    for record in required_records:
        require_regular(record, "required legacy-selected-stage1 record")
    # usage.json is optional for this layout but must be inspected if present.
    if Path("/generation-evidence/usage.json").exists():
        require_regular(Path("/generation-evidence/usage.json"), "optional usage record")
    print("INFO runtime-metrics.json is absent and historically not required for this layout")

    hash_paths = {
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    }
    for key, path in hash_paths.items():
        check_hash(path, audit["hashes"][key], key)

    compare_regular_files(
        Path("/candidate/prompt.py"),
        Path("/reference/prompt.py"),
        "candidate prompt versus trusted prompt",
    )
    compare_regular_files(
        Path("/candidate/py2mpy.py"),
        Path("/reference/py2mpy.py"),
        "candidate translator versus trusted translator",
    )

    trusted_root = Path("/reference/reference-semantics")
    candidate_root = Path("/candidate/reference-semantics")
    trusted_entries = tree_entries(trusted_root)
    candidate_entries = tree_entries(candidate_root)
    assert trusted_entries == candidate_entries, "supplied-semantics trees differ"
    assert all(kind in {"directory", "regular"} for kind, _ in trusted_entries.values())
    assert all(kind in {"directory", "regular"} for kind, _ in candidate_entries.values())
    print(
        "OK recursively identical supplied-semantics trees: "
        f"{sum(k == 'regular' for k, _ in trusted_entries.values())} files, "
        "no symlink/special entries"
    )
    print(
        "INFO reviewer transparent semantics tree digest="
        f"{transparent_tree_digest(trusted_entries)}"
    )
    print("SEMANTICS FILE MANIFEST")
    for rel, (kind, value) in sorted(trusted_entries.items()):
        print(f"  {kind:9s} {value or '-':64s} {rel}")

    candidate_all = tree_entries(Path("/candidate"))
    trace_all = tree_entries(Path("/generation-evidence/codex-trace"))
    assert all(kind != "symlink" for kind, _ in candidate_all.values())
    assert all(kind != "symlink" for kind, _ in trace_all.values())
    print(
        "OK no candidate or trace symlinks; reviewer candidate tree digest="
        f"{transparent_tree_digest(candidate_all)}"
    )
    print(
        "INFO reviewer trace tree digest="
        f"{transparent_tree_digest(trace_all)}"
    )

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    for source_name, record in [
        ("generation-result", result),
        ("invocation", invocation),
    ]:
        evidence = record["outputs"]["evidence"]
        for rel, expected in sorted(evidence.items()):
            path = Path("/generation-evidence") / rel
            check_hash(path, expected, f"{source_name}.outputs.evidence[{rel}]")

    traces = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert traces, "structured trace has no JSONL"
    count = 0
    types: dict[str, int] = {}
    for trace in traces:
        require_regular(trace, "structured trace JSONL")
        with trace.open() as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as err:
                    raise AssertionError(f"{trace}:{line_number}: invalid JSON: {err}")
                count += 1
                event_type = str(obj.get("type", "<missing>"))
                types[event_type] = types.get(event_type, 0) + 1
    print(f"OK parsed structured trace: lines={count}, top-level-types={types}")

    proof_artifacts = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
    ]
    for artifact in proof_artifacts:
        require_regular(artifact, "required candidate proof artifact")
    print("STAGE1_INTEGRITY_OK")


if __name__ == "__main__":
    main()
