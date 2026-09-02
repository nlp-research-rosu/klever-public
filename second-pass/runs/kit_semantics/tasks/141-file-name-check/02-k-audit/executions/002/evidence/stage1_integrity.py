#!/usr/bin/env python3
"""Independent provenance and mounted-tree checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path
from typing import Any


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise ValueError(f"tree root is not a real directory: {root}")
    pending = [root]
    result: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                result.append((relative, "file", path))
            else:
                result.append((relative, "UNSUPPORTED", path))
    return sorted(result)


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the recorded pipeline-v3 tree digest."""
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        if kind == "UNSUPPORTED":
            raise ValueError(f"linked or unsupported entry: {path}")
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise ValueError(f"required JSON is not a regular file: {path}")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"required JSON is not an object: {path}")
    return value


def check_regular(path: Path, errors: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        errors.append(f"missing/unreadable required path {path}: {error}")
        return
    if not stat.S_ISREG(mode):
        errors.append(f"required file is mistyped or symlinked: {path}")


def compare_trees(left: Path, right: Path, errors: list[str]) -> None:
    left_entries = {(rel, kind): path for rel, kind, path in tree_entries(left)}
    right_entries = {(rel, kind): path for rel, kind, path in tree_entries(right)}
    if left_entries.keys() != right_entries.keys():
        errors.append(
            "semantics entry/type mismatch: "
            f"only_trusted={sorted(left_entries.keys() - right_entries.keys())}; "
            f"only_candidate={sorted(right_entries.keys() - left_entries.keys())}"
        )
    for key in sorted(left_entries.keys() & right_entries.keys()):
        if key[1] != "file":
            continue
        left_hash = sha256_file(left_entries[key])
        right_hash = sha256_file(right_entries[key])
        if left_hash != right_hash:
            errors.append(
                f"semantics byte mismatch {key[0]}: "
                f"trusted={left_hash} candidate={right_hash}"
            )


def main() -> int:
    errors: list[str] = []
    audit = load_object(AUDIT_INPUT)
    campaign = load_object(CAMPAIGN_LOCK)

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    if audit.get("record_layout") != "pipeline-v3":
        errors.append("declared record layout is not pipeline-v3")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        errors.append("rendered semantics mode is not SUPPLIED_SEMANTICS")

    expected_campaign_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    actual_campaign_hash = sha256_file(CAMPAIGN_LOCK)
    print(f"campaign_hash_expected={expected_campaign_hash}")
    print(f"campaign_hash_actual={actual_campaign_hash}")
    print(f"campaign_block_equal={audit.get('audit_campaign') == campaign}")
    if expected_campaign_hash != actual_campaign_hash:
        errors.append("campaign-lock hash differs from audit-input")
    if audit.get("audit_campaign") != campaign:
        errors.append("campaign-lock object differs from audit campaign block")

    required_files = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "runtime-metrics.json",
        GENERATION / "usage.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
        REFERENCE / "canonical.py",
        REFERENCE / "prompt.py",
        REFERENCE / "py2mpy.py",
        CANDIDATE / "prompt.py",
        CANDIDATE / "py2mpy.py",
    ]
    for path in required_files:
        check_regular(path, errors)

    direct_hashes = {
        CAMPAIGN_LOCK: audit["hashes"]["audit_campaign_lock_sha256"],
        Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
        Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
        Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
        GENERATION / "invocation.json": audit["hashes"]["stage1_invocation_sha256"],
        GENERATION / "metrics.json": audit["hashes"]["generation_metrics_sha256"],
        GENERATION / "runtime-metrics.json": audit["hashes"][
            "generation_runtime_metrics_sha256"
        ],
        GENERATION / "usage.json": audit["hashes"]["generation_usage_sha256"],
        GENERATION / "codex-last.txt": audit["hashes"][
            "generation_codex_last_sha256"
        ],
        GENERATION / "codex-output.log": audit["hashes"][
            "generation_codex_output_sha256"
        ],
        GENERATION / "prompt.txt": audit["hashes"]["generation_prompt_sha256"],
        REFERENCE / "canonical.py": audit["hashes"]["canonical_sha256"],
        REFERENCE / "prompt.py": audit["hashes"]["trusted_prompt_sha256"],
        REFERENCE / "py2mpy.py": audit["hashes"]["trusted_translator_sha256"],
        CANDIDATE / "prompt.py": audit["hashes"]["candidate_prompt_sha256"],
        CANDIDATE / "py2mpy.py": audit["hashes"]["candidate_translator_sha256"],
    }
    for path, expected in direct_hashes.items():
        actual = sha256_file(path)
        outcome = "MATCH" if actual == expected else "MISMATCH"
        print(f"file_hash {outcome} {path} expected={expected} actual={actual}")
        if actual != expected:
            errors.append(f"recorded file hash mismatch: {path}")

    if (CANDIDATE / "prompt.py").read_bytes() != (
        REFERENCE / "prompt.py"
    ).read_bytes():
        errors.append("candidate prompt differs from trusted prompt")
    if (CANDIDATE / "py2mpy.py").read_bytes() != (
        REFERENCE / "py2mpy.py"
    ).read_bytes():
        errors.append("candidate translator differs from trusted translator")

    trusted_semantics = REFERENCE / "reference-semantics"
    candidate_semantics = CANDIDATE / "reference-semantics"
    for root in (trusted_semantics, candidate_semantics, GENERATION / "codex-trace"):
        try:
            mode = root.lstat().st_mode
            if not stat.S_ISDIR(mode):
                errors.append(f"required tree is not a real directory: {root}")
        except OSError as error:
            errors.append(f"required tree missing/unreadable {root}: {error}")

    compare_trees(trusted_semantics, candidate_semantics, errors)

    task = load_object(Path("/task.json"))
    result = load_object(Path("/generation-result.json"))
    invocation = load_object(GENERATION / "invocation.json")
    usage = load_object(GENERATION / "usage.json")
    embedded_manifest = dict(audit.get("manifest", {}))
    embedded_config = embedded_manifest.pop("config", None)
    print(
        "embedded_manifest_matches_task_after_declared_config="
        f"{embedded_manifest == task and embedded_config == audit.get('manifest_config')}"
    )
    if (
        embedded_manifest != task
        or embedded_config != audit.get("manifest_config")
    ):
        errors.append(
            "audit-input embedded manifest is not /task.json plus manifest_config"
        )

    tree_checks = [
        (
            "trusted-semantics",
            trusted_semantics,
            audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
        ),
        (
            "candidate-semantics",
            candidate_semantics,
            audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
        ),
        (
            "candidate-workspace",
            CANDIDATE,
            result["outputs"]["workspace_sha256"],
        ),
        (
            "trace",
            GENERATION / "codex-trace",
            usage["source_trace_sha256"],
        ),
    ]
    for label, root, expected in tree_checks:
        actual = pipeline_tree_digest(root)
        outcome = "MATCH" if actual == expected else "MISMATCH"
        print(
            f"tree_hash {outcome} {label} expected={expected} actual={actual}"
        )
        if actual != expected:
            errors.append(f"recorded tree hash mismatch: {label}")

    result_evidence = result["outputs"]["evidence"]
    invocation_evidence = invocation["outputs"]["evidence"]
    if result_evidence != invocation_evidence:
        errors.append("generation result and invocation evidence maps differ")
    for relative, expected in sorted(result_evidence.items()):
        path = GENERATION / relative
        check_regular(path, errors)
        if path.exists() and path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            outcome = "MATCH" if actual == expected else "MISMATCH"
            print(
                f"result_evidence_hash {outcome} {relative} "
                f"expected={expected} actual={actual}"
            )
            if actual != expected:
                errors.append(f"generation result evidence mismatch: {relative}")

    trace_files = [
        path
        for relative, kind, path in tree_entries(GENERATION / "codex-trace")
        if kind == "file"
    ]
    json_types: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    event = json.loads(line)
                except ValueError as error:
                    errors.append(f"malformed trace JSON {path}:{line_number}: {error}")
                    continue
                json_types[str(event.get("type", "<missing>"))] += 1
    print(f"trace_files={len(trace_files)} trace_json_lines={trace_lines}")
    print(f"trace_top_level_types={dict(sorted(json_types.items()))}")

    unsupported_candidate = [
        relative
        for relative, kind, _path in tree_entries(CANDIDATE)
        if kind == "UNSUPPORTED"
    ]
    print(f"candidate_unsupported_entries={unsupported_candidate}")
    if unsupported_candidate:
        errors.append("candidate contains symlinked or unsupported entries")

    print(f"ERROR_COUNT={len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
