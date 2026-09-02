#!/usr/bin/env python3
"""Independent, read-only provenance checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-contract tree hash, including paths, kinds, and file sizes."""
    digest = hashlib.sha256()
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
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


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path}: JSON root is not an object"
    return value


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def report_hash(
    label: str, path: Path, expected: str | None, failures: list[str]
) -> None:
    actual = sha256_file(path)
    status = "MATCH" if actual == expected else "MISMATCH"
    print(f"{label}: {status}")
    print(f"  path={path}")
    print(f"  expected={expected}")
    print(f"  actual={actual}")
    if status != "MATCH":
        failures.append(label)


def main() -> None:
    audit = load_object(AUDIT_INPUT)
    lock = load_object(CAMPAIGN_LOCK)
    hashes = audit["hashes"]
    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    failures: list[str] = []

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"problem_id={audit['problem_id']}")

    campaign_equal = audit["audit_campaign"] == lock
    print(f"campaign_block_exact_match={campaign_equal}")
    if not campaign_equal:
        failures.append("campaign block")
    report_hash(
        "audit campaign lock",
        CAMPAIGN_LOCK,
        hashes["audit_campaign_lock_sha256"],
        failures,
    )

    required_files = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        paths["run_manifest"],
        paths["task_manifest"],
        paths["stage1_result"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        paths["generation_last"],
        paths["generation_output"],
        paths["generation_root"] / "prompt.txt",
        paths["generation_root"] / "usage.json",
        paths["canonical"],
        paths["trusted_prompt"],
        paths["translator"],
        paths["candidate"] / "prompt.py",
        paths["candidate"] / "py2mpy.py",
    ]
    for path in required_files:
        require_regular(path)
    for path in [
        paths["candidate"],
        paths["generation_root"],
        paths["generation_trace"],
        paths["canonical"].parent,
    ]:
        require_directory(path)

    # Parse all launcher JSON and every line of the structured trace.
    json_paths = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        paths["run_manifest"],
        paths["task_manifest"],
        paths["stage1_result"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        paths["generation_root"] / "usage.json",
        paths["generation_root"] / "legacy-metrics.json",
        paths["generation_root"] / "legacy-run-input.json",
    ]
    for path in json_paths:
        if path.exists():
            load_object(path)
            print(f"parsed_json={path}")

    trace_files = sorted(paths["generation_trace"].rglob("*"))
    trace_regular = [path for path in trace_files if path.is_file()]
    trace_lines = 0
    trace_types: dict[str, int] = {}
    for path in trace_files:
        mode = path.lstat().st_mode
        assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), (
            f"linked or unsupported trace entry: {path}"
        )
    for path in trace_regular:
        require_regular(path)
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                item = json.loads(line)
                assert isinstance(item, dict), f"{path}:{line_number}: not an object"
                item_type = str(item.get("type", "<missing>"))
                trace_types[item_type] = trace_types.get(item_type, 0) + 1
                trace_lines += 1
    print(f"trace_files={len(trace_regular)}")
    print(f"trace_json_objects={trace_lines}")
    print(f"trace_top_level_types={json.dumps(trace_types, sort_keys=True)}")

    expected_map = [
        ("run manifest", paths["run_manifest"], hashes["run_manifest_sha256"]),
        ("task manifest", paths["task_manifest"], hashes["task_manifest_sha256"]),
        ("stage1 result", paths["stage1_result"], hashes["stage1_result_sha256"]),
        (
            "stage1 invocation",
            paths["generation_manifest"],
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation metrics",
            paths["generation_metrics"],
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation usage",
            paths["generation_root"] / "usage.json",
            hashes["generation_usage_sha256"],
        ),
        (
            "generation final",
            paths["generation_last"],
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation output",
            paths["generation_output"],
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation prompt",
            paths["generation_root"] / "prompt.txt",
            hashes["generation_prompt_sha256"],
        ),
        ("canonical", paths["canonical"], hashes["canonical_sha256"]),
        ("trusted prompt", paths["trusted_prompt"], hashes["trusted_prompt_sha256"]),
        ("translator", paths["translator"], hashes["trusted_translator_sha256"]),
        (
            "candidate prompt",
            paths["candidate"] / "prompt.py",
            hashes["candidate_prompt_sha256"],
        ),
        (
            "candidate translator",
            paths["candidate"] / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
    ]
    for label, path, expected in expected_map:
        report_hash(label, path, expected, failures)

    result = load_object(paths["stage1_result"])
    invocation = load_object(paths["generation_manifest"])
    for record_name, record in [("result", result), ("invocation", invocation)]:
        evidence = record["outputs"]["evidence"]
        for relative, expected in sorted(evidence.items()):
            report_hash(
                f"{record_name} evidence {relative}",
                paths["generation_root"] / relative,
                expected,
                failures,
            )

    usage = load_object(paths["generation_root"] / "usage.json")
    trace_hash = sha256_tree(paths["generation_trace"])
    print("generation trace pipeline tree hash:")
    print(f"  usage_expected={usage['source_trace_sha256']}")
    print(f"  actual={trace_hash}")
    print(
        "  audit_input_secondary_digest="
        + str(hashes["generation_codex_trace_sha256"])
    )
    if trace_hash != usage["source_trace_sha256"]:
        failures.append("generation trace pipeline tree")

    candidate_hash = sha256_tree(paths["candidate"])
    generation_workspace_hash = result["outputs"]["workspace_sha256"]
    invocation_workspace_hash = invocation["outputs"]["workspace_sha256"]
    print("candidate pipeline tree hash:")
    print(f"  actual={candidate_hash}")
    print(f"  generation_result_expected={generation_workspace_hash}")
    print(f"  invocation_expected={invocation_workspace_hash}")
    print(f"  audit_input_secondary_digest={hashes['candidate_tree_sha256']}")
    if candidate_hash not in {generation_workspace_hash, invocation_workspace_hash}:
        failures.append("candidate pipeline tree")

    # GENERATED_SEMANTICS requires no trusted reference-semantics mount.
    hidden_semantics = paths["canonical"].parent / "reference-semantics"
    print(f"trusted_reference_semantics_exists={hidden_semantics.exists()}")
    print(
        "generated_semantics_null_fields="
        + str(
            audit["reference_semantics"] is None
            and hashes["trusted_reference_semantics_sha256"] is None
            and hashes["candidate_reference_semantics_sha256"] is None
        )
    )
    if hidden_semantics.exists():
        failures.append("unexpected trusted reference semantics")

    candidate_entries = sorted(paths["candidate"].iterdir())
    print("candidate_entries=" + ",".join(path.name for path in candidate_entries))
    for path in candidate_entries:
        require_regular(path)

    print("FAILURES=" + (",".join(failures) if failures else "NONE"))
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
