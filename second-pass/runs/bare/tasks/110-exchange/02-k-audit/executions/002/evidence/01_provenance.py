#!/usr/bin/env python3
"""Independent provenance/type/hash checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the length-delimited tree digest used in stage-1 records."""
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise AssertionError(f"tree root is not a real directory: {root}")
    digest = hashlib.sha256()
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


def require_file(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    print(f"TYPE_OK file {path}")


def require_dir(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    print(f"TYPE_OK directory {path}")


def load_object(path: Path) -> dict:
    require_file(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"JSON root is not an object: {path}"
    return value


def compare_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    assert actual == expected, (label, expected, actual)
    print(f"HASH_OK {label} {actual} {path}")


def main() -> int:
    audit = load_object(AUDIT_INPUT)
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["problem_id"] == "110-exchange"
    assert audit["condition"] == "bare"
    print("DECLARATION_OK legacy-selected-stage1 GENERATED_SEMANTICS bare 110-exchange")

    required_files = [
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    required_dirs = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference"),
    ]
    for path in required_files:
        require_file(path)
    for path in required_dirs:
        require_dir(path)

    usage_path = Path("/generation-evidence/usage.json")
    if usage_path.exists() or usage_path.is_symlink():
        require_file(usage_path)
        print("OPTIONAL_PRESENT usage.json")
    else:
        print("OPTIONAL_ABSENT usage.json")
    runtime_path = Path("/generation-evidence/runtime-metrics.json")
    if runtime_path.exists() or runtime_path.is_symlink():
        require_file(runtime_path)
        print("OPTIONAL_PRESENT runtime-metrics.json")
    else:
        print("EXPECTED_LEGACY_ABSENCE runtime-metrics.json")

    forbidden_semantics = Path("/reference/reference-semantics")
    assert not forbidden_semantics.exists() and not forbidden_semantics.is_symlink()
    print("SEMANTICS_BOUNDARY_OK trusted reference-semantics absent")

    lock = load_object(Path("/audit-campaign-lock.json"))
    assert lock == audit["audit_campaign"]
    print("CAMPAIGN_CONTENT_OK lock exactly equals audit_campaign")

    hashes = audit["hashes"]
    fixed_hashes = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
    }
    if hashes.get("generation_usage_sha256") is not None:
        fixed_hashes["generation_usage_sha256"] = usage_path
    for label, path in fixed_hashes.items():
        compare_hash(label, path, hashes[label])

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("TRUSTED_COPY_OK candidate prompt.py and py2mpy.py byte-identical")

    run = load_object(Path("/run.json"))
    task = load_object(Path("/task.json"))
    result = load_object(Path("/generation-result.json"))
    invocation = load_object(Path("/generation-evidence/invocation.json"))
    metrics = load_object(Path("/generation-evidence/metrics.json"))
    usage = load_object(usage_path)
    audit_manifest = dict(audit["manifest"])
    audit_manifest_config = audit_manifest.pop("config")
    assert task == audit_manifest
    assert audit_manifest_config == audit["manifest_config"] == audit["config"]
    assert run["run_id"] == audit["run_id"]
    assert run["config"] == audit["config"]
    assert task["problem_id"] == audit["problem_id"]
    assert task["condition"]["name"] == audit["condition"]
    assert result["invocation"] == invocation["name"] == "001-initial"
    assert result["status"] == invocation["status"] == metrics["status"] == "SUCCEEDED"
    assert result["result_marker"] == invocation["result_marker"] == "KPROVE_PASSED"
    print("RECORD_CROSSCHECK_OK run/task/result/invocation/metrics")

    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / relative
        require_file(path)
        compare_hash(f"generation-result:{relative}", path, expected)
        assert invocation["outputs"]["evidence"][relative] == expected
    print("GENERATION_EVIDENCE_MAP_OK all result/invocation evidence entries")

    candidate_tree = pipeline_tree_digest(Path("/candidate"))
    trace_tree = pipeline_tree_digest(Path("/generation-evidence/codex-trace"))
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    assert candidate_tree == invocation["retained_workspace_sha256"]
    assert trace_tree == usage["source_trace_sha256"]
    print(f"TREE_HASH_OK stage1-workspace {candidate_tree}")
    print(f"TREE_HASH_OK usage-source-trace {trace_tree}")
    print(
        "LAUNCHER_DECLARED_TREE_HASHES "
        f"candidate={hashes['candidate_tree_sha256']} "
        f"trace={hashes['generation_codex_trace_sha256']}"
    )
    print(
        "NOTE launcher tree fields use a different framing from the independently "
        "reconstructed stage-1/usage tree digest; per-file and source-record "
        "digests above are authoritative byte checks"
    )

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    regular_trace_files = [path for path in trace_files if path.is_file()]
    assert len(regular_trace_files) == 1
    trace_path = regular_trace_files[0]
    rows = []
    with trace_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            row = json.loads(line)
            assert isinstance(row, dict)
            rows.append(row)
    assert len(rows) == 159
    assert rows[0]["payload"]["session_id"] == result["session_id"]
    assert rows[-1]["payload"]["type"] == "task_complete"
    selected_line = usage["selected_event"]["line_number"]
    selected = rows[selected_line - 1]
    assert selected["payload"]["type"] == "token_count"
    print(
        f"TRACE_PARSE_OK files=1 rows={len(rows)} "
        f"session={result['session_id']} selected_usage_line={selected_line}"
    )

    print("INDIVIDUAL_CANDIDATE_HASHES")
    for path in sorted(Path("/candidate").rglob("*")):
        mode = path.lstat().st_mode
        assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), f"unsupported candidate entry: {path}"
        if stat.S_ISREG(mode):
            print(
                f"FILE {path.relative_to('/candidate').as_posix()} "
                f"{path.stat().st_size} {sha256_file(path)}"
            )

    print("PROVENANCE_CHECK_COMPLETE")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"PROVENANCE_CHECK_FAILED {type(error).__name__}: {error}", file=sys.stderr)
        raise
