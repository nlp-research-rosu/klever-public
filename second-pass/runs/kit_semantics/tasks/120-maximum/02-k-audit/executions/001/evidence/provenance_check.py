#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    assert not path.is_symlink(), f"symlinked directory: {path}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            elif stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            else:
                result[relative] = ("unsupported", oct(mode))
    return result


def manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(
        sorted((path, kind, value) for path, (kind, value) in entries.items()),
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Independently reproduce pipeline-v3's length-delimited tree digest."""
    root = root.resolve(strict=True)
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
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
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"problem_id={audit['problem_id']}")
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["problem_id"] == "120-maximum"
    assert audit["mount_reference_semantics"] is True

    assert audit["audit_campaign"] == lock
    print("campaign_block_match=true")
    actual_lock_hash = sha256_file(LOCK)
    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"audit_campaign_lock_sha256={actual_lock_hash}")
    assert actual_lock_hash == expected_lock_hash

    required_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    required_dirs = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_dirs:
        require_directory(path)
    print(f"required_regular_files={len(required_files)}")
    print(f"required_real_directories={len(required_dirs)}")

    expected_hashes = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/runtime-metrics.json"):
            "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"):
            "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"):
            "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, key in expected_hashes.items():
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        print(f"{path} sha256={actual} expected={expected} match={actual == expected}")
        assert actual == expected

    records = {
        path.as_posix(): json.loads(path.read_text(encoding="utf-8"))
        for path in required_files
        if path.suffix == ".json"
    }
    assert records["/task.json"]["problem_id"] == "120-maximum"
    assert records["/task.json"]["condition"]["name"] == "kit-semantics"
    assert records["/generation-result.json"]["status"] == "SUCCEEDED"
    assert records["/generation-evidence/invocation.json"]["status"] == "SUCCEEDED"
    assert records["/generation-evidence/metrics.json"]["status"] == "SUCCEEDED"
    assert records["/generation-evidence/runtime-metrics.json"]["final_exit_code"] == 0
    assert records["/generation-evidence/usage.json"]["status"] == "COMPLETE"
    print("required_json_parse_and_fields=true")

    candidate_pipeline_digest = pipeline_tree_digest(Path("/candidate"))
    expected_candidate_pipeline_digest = records["/generation-result.json"]["outputs"][
        "workspace_sha256"
    ]
    print(
        "candidate_pipeline_tree_sha256="
        f"{candidate_pipeline_digest} expected={expected_candidate_pipeline_digest} "
        f"match={candidate_pipeline_digest == expected_candidate_pipeline_digest}"
    )
    assert candidate_pipeline_digest == expected_candidate_pipeline_digest

    candidate_prompt = Path("/candidate/prompt.py")
    candidate_translator = Path("/candidate/py2mpy.py")
    require_regular(candidate_prompt)
    require_regular(candidate_translator)
    prompt_match = candidate_prompt.read_bytes() == Path("/reference/prompt.py").read_bytes()
    translator_match = (
        candidate_translator.read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"candidate_prompt_matches_trusted={prompt_match}")
    print(f"candidate_translator_matches_trusted={translator_match}")
    assert prompt_match and translator_match

    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
    print(f"trusted_semantics_entries={len(trusted_semantics)}")
    print(f"candidate_semantics_entries={len(candidate_semantics)}")
    print(f"trusted_semantics_manifest_sha256={manifest_digest(trusted_semantics)}")
    print(f"candidate_semantics_manifest_sha256={manifest_digest(candidate_semantics)}")
    assert all(kind != "symlink" for kind, _ in candidate_semantics.values())
    assert trusted_semantics == candidate_semantics
    print("candidate_reference_semantics_exact_tree_match=true")
    semantics_pipeline_digest = pipeline_tree_digest(
        Path("/candidate/reference-semantics")
    )
    expected_semantics_pipeline_digest = records["/task.json"]["inputs"][
        "reference_semantics_sha256"
    ]
    print(
        "candidate_reference_semantics_pipeline_sha256="
        f"{semantics_pipeline_digest} expected={expected_semantics_pipeline_digest} "
        f"match={semantics_pipeline_digest == expected_semantics_pipeline_digest}"
    )
    assert semantics_pipeline_digest == expected_semantics_pipeline_digest

    proof_files = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
    ]
    for path in proof_files:
        require_regular(path)
    print(f"required_candidate_proof_files={len(proof_files)}")

    result = records["/generation-result.json"]
    trace_root = Path("/generation-evidence/codex-trace")
    trace_entries = tree_entries(trace_root)
    assert all(kind in {"directory", "file"} for kind, _ in trace_entries.values())
    trace_files = sorted(
        path for path, (kind, _) in trace_entries.items() if kind == "file"
    )
    assert trace_files
    print(f"trace_files={len(trace_files)}")
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    trace_line_count = 0
    for relative in trace_files:
        path = trace_root / relative
        evidence_key = f"codex-trace/{relative}"
        expected = result["outputs"]["evidence"][evidence_key]
        actual = sha256_file(path)
        print(f"{path} sha256={actual} expected={expected} match={actual == expected}")
        assert actual == expected
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                event = json.loads(line)
                trace_line_count += 1
                event_types[str(event.get("type", "<missing>"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type", "<missing>"))] += 1
                assert isinstance(event, dict), f"non-object trace event {path}:{line_number}"
    print(f"trace_jsonl_records={trace_line_count}")
    print(f"trace_top_level_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    trace_pipeline_digest = pipeline_tree_digest(trace_root)
    expected_trace_pipeline_digest = records["/generation-evidence/usage.json"][
        "source_trace_sha256"
    ]
    print(
        "trace_pipeline_tree_sha256="
        f"{trace_pipeline_digest} expected={expected_trace_pipeline_digest} "
        f"match={trace_pipeline_digest == expected_trace_pipeline_digest}"
    )
    assert trace_pipeline_digest == expected_trace_pipeline_digest
    print("PROVENANCE_CHECK_PASSED")


if __name__ == "__main__":
    main()
