#!/usr/bin/env python3
"""Independent integrity and generation-record inspection for this audit."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def real_file(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def real_dir(path: Path) -> bool:
    return path.is_dir() and not path.is_symlink()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if not real_dir(root):
        raise RuntimeError(f"tree root is not a real directory: {root}")
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
    return sorted(entries)


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce the length-delimited digest used in retained workspace records."""
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
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


def read_object(path: Path) -> dict:
    if not real_file(path):
        raise RuntimeError(f"missing, linked, or mistyped JSON file: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root is not an object: {path}")
    return value


def check_equal(label: str, actual: object, expected: object) -> None:
    state = "OK" if actual == expected else "MISMATCH"
    print(f"{state} {label}: actual={actual!r} expected={expected!r}")
    if state != "OK":
        raise RuntimeError(f"{label} mismatch")


def main() -> int:
    audit = read_object(AUDIT_INPUT)
    lock = read_object(CAMPAIGN_LOCK)
    check_equal("record layout", audit.get("record_layout"), "legacy-selected-stage1")
    check_equal("semantics mode", audit.get("semantics_mode"), "GENERATED_SEMANTICS")
    check_equal("campaign block", lock, audit.get("audit_campaign"))
    check_equal(
        "campaign lock sha256",
        sha256_file(CAMPAIGN_LOCK),
        audit["hashes"]["audit_campaign_lock_sha256"],
    )

    required_files = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    required_dirs = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    print("REQUIRED RECORD TYPES")
    for path in required_files:
        if not real_file(path):
            raise RuntimeError(f"missing, linked, or mistyped required file: {path}")
        print(f"OK regular-file {path}")
    for path in required_dirs:
        if not real_dir(path):
            raise RuntimeError(f"missing, linked, or mistyped required directory: {path}")
        print(f"OK directory {path}")
        tree_entries(path)

    if Path("/reference/reference-semantics").exists() or Path(
        "/reference/reference-semantics"
    ).is_symlink():
        raise RuntimeError("GENERATED_SEMANTICS mode has forbidden reference semantics")
    print("OK GENERATED_SEMANTICS boundary: /reference/reference-semantics absent")

    candidate_required = [
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for relative in candidate_required:
        path = Path("/candidate") / relative
        if not real_file(path):
            raise RuntimeError(f"candidate artifact missing, linked, or mistyped: {path}")
        print(f"OK candidate artifact {path}")

    hashes = audit["hashes"]
    file_hash_checks = {
        "/run.json": hashes["run_manifest_sha256"],
        "/task.json": hashes["task_manifest_sha256"],
        "/generation-result.json": hashes["stage1_result_sha256"],
        "/generation-evidence/invocation.json": hashes["stage1_invocation_sha256"],
        "/generation-evidence/metrics.json": hashes["generation_metrics_sha256"],
        "/generation-evidence/usage.json": hashes["generation_usage_sha256"],
        "/generation-evidence/codex-last.txt": hashes["generation_codex_last_sha256"],
        "/generation-evidence/codex-output.log": hashes["generation_codex_output_sha256"],
        "/generation-evidence/prompt.txt": hashes["generation_prompt_sha256"],
        "/reference/canonical.py": hashes["canonical_sha256"],
        "/reference/prompt.py": hashes["trusted_prompt_sha256"],
        "/reference/py2mpy.py": hashes["trusted_translator_sha256"],
        "/candidate/prompt.py": hashes["candidate_prompt_sha256"],
        "/candidate/py2mpy.py": hashes["candidate_translator_sha256"],
    }
    print("RECORDED FILE HASHES")
    for raw_path, expected in file_hash_checks.items():
        path = Path(raw_path)
        if not real_file(path):
            raise RuntimeError(f"hashed file missing, linked, or mistyped: {path}")
        check_equal(f"sha256 {path}", sha256_file(path), expected)

    check_equal(
        "candidate prompt byte identity",
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes(),
        True,
    )
    check_equal(
        "candidate translator byte identity",
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes(),
        True,
    )

    run = read_object(Path("/run.json"))
    task = read_object(Path("/task.json"))
    result = read_object(Path("/generation-result.json"))
    invocation = read_object(Path("/generation-evidence/invocation.json"))
    metrics = read_object(Path("/generation-evidence/metrics.json"))
    usage = read_object(Path("/generation-evidence/usage.json"))
    read_object(Path("/generation-evidence/legacy-metrics.json"))
    read_object(Path("/generation-evidence/legacy-run-input.json"))
    audit_manifest = audit["manifest"]
    for key in ("condition", "current_stage", "input_provenance", "inputs",
                "problem_id", "schema_version"):
        check_equal(f"task manifest field {key}", task.get(key), audit_manifest.get(key))
    check_equal("audit manifest config", audit_manifest.get("config"), audit["config"])
    check_equal("run config", run.get("config"), audit["config"])
    check_equal("task problem", task.get("problem_id"), audit["problem_id"])
    check_equal("invocation session", invocation.get("session_id"), result.get("session_id"))
    check_equal("invocation duration", invocation.get("duration_s"), metrics.get("duration_s"))

    evidence_expected = result["outputs"]["evidence"]
    print("GENERATION RESULT EVIDENCE HASHES")
    for relative, expected in sorted(evidence_expected.items()):
        path = Path("/generation-evidence") / relative
        if not real_file(path):
            raise RuntimeError(f"generation evidence missing or mistyped: {path}")
        check_equal(f"generation evidence {relative}", sha256_file(path), expected)

    candidate_tree = pipeline_tree_digest(Path("/candidate"))
    trace_tree = pipeline_tree_digest(Path("/generation-evidence/codex-trace"))
    check_equal(
        "retained candidate workspace tree digest",
        candidate_tree,
        result["outputs"]["workspace_sha256"],
    )
    check_equal(
        "invocation candidate workspace tree digest",
        candidate_tree,
        invocation["retained_workspace_sha256"],
    )
    check_equal(
        "usage source trace tree digest",
        trace_tree,
        usage["source_trace_sha256"],
    )
    print(
        "INFO launcher-declared alternate candidate tree digest "
        f"{hashes['candidate_tree_sha256']}"
    )
    print(
        "INFO launcher-declared alternate trace tree digest "
        f"{hashes['generation_codex_trace_sha256']}"
    )

    prompt_hash = sha256_file(Path("/generation-evidence/prompt.txt"))
    check_equal("invocation prompt sha256", prompt_hash, invocation["prompt_sha256"])
    check_equal(
        "task instruction prompt sha256",
        prompt_hash,
        task["inputs"]["instruction_prompt_sha256"],
    )

    trace_files = [
        path for _relative, kind, path in tree_entries(Path("/generation-evidence/codex-trace"))
        if kind == "file"
    ]
    if not trace_files:
        raise RuntimeError("structured trace contains no files")
    outer_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    function_calls: list[tuple[int, str, str]] = []
    total_trace_lines = 0
    first_timestamp = None
    last_timestamp = None
    for trace_path in trace_files:
        with trace_path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_trace_lines += 1
                event = json.loads(line)
                outer_types[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_type = str(payload.get("type"))
                    payload_types[payload_type] += 1
                    role = payload.get("role")
                    if role is not None:
                        roles[str(role)] += 1
                    if payload_type in {"function_call", "custom_tool_call"}:
                        name = str(payload.get("name"))
                        arguments = str(payload.get("arguments") or payload.get("input"))
                        function_calls.append((line_number, name, arguments))
                timestamp = event.get("timestamp")
                if first_timestamp is None:
                    first_timestamp = timestamp
                last_timestamp = timestamp

    print("STRUCTURED TRACE SUMMARY")
    print(f"trace_files={len(trace_files)} trace_lines={total_trace_lines}")
    print(f"first_timestamp={first_timestamp} last_timestamp={last_timestamp}")
    print(f"outer_types={dict(sorted(outer_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"roles={dict(sorted(roles.items()))}")
    print(f"function_call_count={len(function_calls)}")
    for line_number, name, arguments in function_calls:
        compact = " ".join(arguments.split())
        print(f"trace_call line={line_number} name={name} args={compact[:600]}")

    selected = usage["selected_event"]
    selected_path = Path("/generation-evidence/codex-trace") / selected["relative_path"]
    with selected_path.open(encoding="utf-8") as stream:
        selected_line = next(
            line for number, line in enumerate(stream, 1)
            if number == selected["line_number"]
        )
    selected_event = json.loads(selected_line)
    selected_payload = selected_event.get("payload", {})
    check_equal("usage selected event type", selected_payload.get("type"), "token_count")

    output_path = Path("/generation-evidence/codex-output.log")
    output_lines = 0
    output_top_lines = 0
    output_markers = 0
    with output_path.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            output_lines += 1
            if line.strip() == "#Top":
                output_top_lines += 1
            if "RESULT: KPROVE_PASSED" in line:
                output_markers += 1
    print("GENERATION OUTPUT SUMMARY (UNTRUSTED)")
    print(
        f"lines={output_lines} exact_top_lines={output_top_lines} "
        f"kprove_passed_marker_lines={output_markers}"
    )

    mounts = [
        "/candidate",
        "/generation-evidence",
        "/audit-input.json",
        "/audit-campaign-lock.json",
        "/run.json",
        "/task.json",
        "/generation-result.json",
        "/reference/canonical.py",
        "/reference/prompt.py",
        "/reference/py2mpy.py",
    ]
    print("MOUNT OPTIONS")
    for path in mounts:
        result_process = subprocess.run(
            ["findmnt", "-T", path, "-n", "-o", "OPTIONS"],
            check=True,
            capture_output=True,
            text=True,
        )
        options = result_process.stdout.strip()
        print(f"{path}: {options}")
        if "ro" not in options.split(","):
            raise RuntimeError(f"launcher-declared input is not read-only: {path}")

    print("STAGE1_INTEGRITY: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"STAGE1_INTEGRITY: ERROR: {error}", file=sys.stderr)
        raise
