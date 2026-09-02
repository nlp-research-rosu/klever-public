#!/usr/bin/env python3
"""Independent type, hash, and provenance checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
REQUIRED_PIPELINE_V3 = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation/invocation.json"),
    Path("/generation/metrics.json"),
    Path("/generation/runtime-metrics.json"),
    Path("/generation/usage.json"),
    Path("/generation/codex-last.txt"),
    Path("/generation/codex-output.log"),
    Path("/generation/prompt.txt"),
]
REQUIRED_CANDIDATE = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
    "prompt.py",
    "py2mpy.py",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and not stat.S_ISLNK(mode)


def file_manifest(root: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries.append({"path": rel, "type": "symlink", "target": os.readlink(path)})
        elif stat.S_ISDIR(mode):
            entries.append({"path": rel, "type": "directory"})
        elif stat.S_ISREG(mode):
            entries.append(
                {
                    "path": rel,
                    "type": "file",
                    "size": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
        else:
            entries.append({"path": rel, "type": "other", "mode": mode})
    return entries


def compare_trees(left: Path, right: Path) -> list[str]:
    differences: list[str] = []
    left_entries = {item["path"]: item for item in file_manifest(left)}
    right_entries = {item["path"]: item for item in file_manifest(right)}
    for rel in sorted(left_entries.keys() | right_entries.keys()):
        a = left_entries.get(rel)
        b = right_entries.get(rel)
        if a is None:
            differences.append(f"additional candidate entry: {rel}")
        elif b is None:
            differences.append(f"missing candidate entry: {rel}")
        elif a != b:
            differences.append(f"entry differs: {rel}: trusted={a!r} candidate={b!r}")
    return differences


def main() -> int:
    failures: list[str] = []
    data = json.loads(AUDIT.read_text())
    print(f"record_layout={data.get('record_layout')}")
    print(f"semantics_mode={data.get('semantics_mode')}")
    if data.get("record_layout") != "pipeline-v3":
        failures.append("declared layout is not pipeline-v3")
    if data.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("declared mode is not SUPPLIED_SEMANTICS")

    for path in [AUDIT, *REQUIRED_PIPELINE_V3]:
        ok = regular_nonsymlink(path)
        print(f"required_regular_file {path}: {ok}")
        if not ok:
            failures.append(f"missing, unreadable, mistyped, or symlinked record: {path}")
        elif path.suffix == ".json":
            record = json.loads(path.read_text())
            print(f"record_keys {path}: {sorted(record)}")
        else:
            with path.open(errors="replace") as stream:
                line_count = sum(1 for _ in stream)
            print(f"text_record_size {path}: bytes={path.stat().st_size} lines={line_count}")

    trace_root = Path("/generation/codex-trace")
    trace_files = sorted(trace_root.rglob("*.jsonl")) if trace_root.is_dir() else []
    print(f"trace_files={len(trace_files)}")
    if not trace_files:
        failures.append("structured trace is absent")
    for trace in trace_files:
        invalid: list[int] = []
        lines = 0
        top_types: Counter[str] = Counter()
        payload_types: Counter[str] = Counter()
        with trace.open() as stream:
            for lines, line in enumerate(stream, 1):
                try:
                    event = json.loads(line)
                    top_types[str(event.get("type"))] += 1
                    payload = event.get("payload")
                    if isinstance(payload, dict):
                        payload_types[str(payload.get("type"))] += 1
                except json.JSONDecodeError:
                    invalid.append(lines)
        print(
            f"trace {trace.relative_to(trace_root)} lines={lines} "
            f"invalid_json_lines={invalid} sha256={sha256(trace)}"
        )
        print(f"trace_top_level_types={dict(sorted(top_types.items()))}")
        print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
        if invalid:
            failures.append(f"invalid JSONL in {trace}: {invalid}")

    expected_direct = {
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation/invocation.json": "stage1_invocation_sha256",
        "/generation/metrics.json": "generation_metrics_sha256",
        "/generation/runtime-metrics.json": "generation_runtime_metrics_sha256",
        "/generation/usage.json": "generation_usage_sha256",
        "/generation/codex-last.txt": "generation_codex_last_sha256",
        "/generation/codex-output.log": "generation_codex_output_sha256",
        "/generation/prompt.txt": "generation_prompt_sha256",
    }
    recorded = data["hashes"]
    for name, key in expected_direct.items():
        path = Path(name)
        actual = sha256(path)
        expected = recorded[key]
        ok = actual == expected
        print(f"recorded_hash {name}: expected={expected} actual={actual} match={ok}")
        if not ok:
            failures.append(f"recorded hash mismatch: {name}")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation/invocation.json").read_text())
    for source_name, source in (("generation-result", result), ("invocation", invocation)):
        for rel, expected in sorted(source["outputs"]["evidence"].items()):
            path = Path("/generation") / rel
            ok_type = regular_nonsymlink(path)
            actual = sha256(path) if ok_type else "<unavailable>"
            ok = ok_type and actual == expected
            print(
                f"{source_name}_evidence_hash {rel}: expected={expected} "
                f"actual={actual} match={ok}"
            )
            if not ok:
                failures.append(f"{source_name} evidence mismatch: {rel}")

    candidate = Path("/candidate")
    for rel in REQUIRED_CANDIDATE:
        path = candidate / rel
        ok = regular_nonsymlink(path)
        print(f"candidate_required_regular_file {rel}: {ok}")
        if not ok:
            failures.append(f"candidate proof artifact absent or mistyped: {rel}")

    if not Path("/reference/reference-semantics").is_dir():
        failures.append("trusted reference semantics absent in SUPPLIED_SEMANTICS mode")
    if not Path("/candidate/reference-semantics").is_dir():
        failures.append("candidate reference semantics absent")
    tree_differences = compare_trees(
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    )
    print(f"semantics_tree_differences={len(tree_differences)}")
    for difference in tree_differences:
        print(difference)
    failures.extend(tree_differences)

    prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not prompt_equal:
        failures.append("candidate prompt changed")
    if not translator_equal:
        failures.append("candidate translator changed")

    for root in [
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
        Path("/generation/codex-trace"),
        Path("/candidate"),
    ]:
        manifest = file_manifest(root)
        serialized = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
        print(
            f"independent_manifest {root}: entries={len(manifest)} "
            f"sha256={hashlib.sha256(serialized).hexdigest()}"
        )
        symlinks = [entry for entry in manifest if entry["type"] == "symlink"]
        print(f"symlinks {root}: {symlinks}")
        if root != Path("/candidate") and symlinks:
            failures.append(f"unexpected symlinks below {root}")

    print(f"failures={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
