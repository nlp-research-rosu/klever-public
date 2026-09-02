#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pipeline_content_tree_sha256(root: Path) -> str:
    """Path/type/size/content digest used by the stage-1 pipeline records."""
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
                raise AssertionError(f"unsupported or linked tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.is_file() and not path.is_symlink(), path
    path.read_bytes()


def require_directory(path: Path) -> None:
    assert path.is_dir() and not path.is_symlink(), path


def main() -> None:
    audit_path = Path("/audit-input.json")
    lock_path = Path("/audit-campaign-lock.json")
    audit = json.loads(audit_path.read_text())
    lock = json.loads(lock_path.read_text())

    print(f"AUDIT_INPUT_SHA256 {sha256_file(audit_path)}")
    print(f"RECORD_LAYOUT {audit['record_layout']}")
    print(f"SEMANTICS_MODE {audit['semantics_mode']}")
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    assert sha256_file(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"]
    print("CAMPAIGN_BLOCK_EQUAL true")
    print("CAMPAIGN_LOCK_HASH_MATCH true")
    print(f"INTEGRITY_FIELDS {audit['integrity']}")
    assert audit["integrity"] == {
        "candidate_prompt_matches_trusted": True,
        "candidate_reference_semantics_matches_trusted": None,
        "candidate_translator_matches_trusted": True,
        "manifest_prompt_hash_matches_trusted": True,
        "manifest_reference_semantics_hash_matches_trusted": None,
        "manifest_translator_hash_matches_trusted": True,
    }
    for name, mounted_value in sorted(audit["container_paths"].items()):
        mounted = Path(mounted_value)
        assert mounted.exists(), (name, mounted)
        assert not mounted.is_symlink(), (name, mounted)
        print(f"CONTAINER_PATH_OK {name} {mounted}")

    required_files = [
        Path("/audit-input.json"),
        lock_path,
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
    for path in required_files:
        require_regular(path)
        print(f"REQUIRED_FILE_OK {path}")
    for json_record in (
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
    ):
        parsed = json.loads(json_record.read_text())
        assert isinstance(parsed, dict)
        print(f"JSON_OBJECT_PARSED {json_record}")
    require_directory(Path("/candidate"))
    require_directory(Path("/generation-evidence/codex-trace"))

    # usage.json is optional for this historical layout, but is present.
    usage = Path("/generation-evidence/usage.json")
    require_regular(usage)
    print("OPTIONAL_USAGE_PRESENT true")
    print(
        "EXPECTED_LEGACY_RUNTIME_METRICS_ABSENT "
        f"{not Path('/generation-evidence/runtime-metrics.json').exists()}"
    )
    for optional_legacy in (
        Path("/generation-evidence/legacy-metrics.json"),
        Path("/generation-evidence/legacy-run-input.json"),
    ):
        require_regular(optional_legacy)
        print(f"LEGACY_RECORD_OK {optional_legacy}")

    expected_files = {
        lock_path: "audit_campaign_lock_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        usage: "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"):
            "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"):
            "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    }
    for path, key in expected_files.items():
        observed = sha256_file(path)
        expected = audit["hashes"][key]
        assert observed == expected, (path, key, observed, expected)
        print(f"HASH_MATCH {key} {observed} {path}")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("CANDIDATE_PROMPT_BYTE_IDENTICAL true")
    print("CANDIDATE_TRANSLATOR_BYTE_IDENTICAL true")

    assert not Path("/reference/reference-semantics").exists()
    assert not Path("/candidate/reference-semantics").exists()
    print("GENERATED_MODE_REFERENCE_SEMANTICS_ABSENT true")

    # Inspect every candidate entry without trusting the recorded tree claim.
    candidate_entries = sorted(Path("/candidate").rglob("*"))
    for path in candidate_entries:
        mode = path.stat(follow_symlinks=False).st_mode
        assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), path
        assert not path.is_symlink(), path
        print(
            f"CANDIDATE_ENTRY "
            f"{'file' if stat.S_ISREG(mode) else 'directory'} "
            f"{path.relative_to('/candidate')}"
        )

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        if relative.startswith("codex-trace/"):
            continue
        mounted_name = {
            "legacy-metrics.json": "legacy-metrics.json",
            "legacy-run-input.json": "legacy-run-input.json",
        }.get(relative, relative)
        mounted = Path("/generation-evidence") / mounted_name
        require_regular(mounted)
        observed = sha256_file(mounted)
        assert observed == expected, (relative, observed, expected)
        print(f"GENERATION_RESULT_EVIDENCE_HASH_MATCH {relative} {observed}")
    candidate_digest = pipeline_content_tree_sha256(Path("/candidate"))
    declared_workspace = result["outputs"]["workspace_sha256"]
    assert candidate_digest == declared_workspace
    assert candidate_digest == invocation["retained_workspace_sha256"]
    print(f"CANDIDATE_PIPELINE_CONTENT_TREE_SHA256 {candidate_digest}")
    print(f"AUDIT_RECORDED_CANDIDATE_TREE_SHA256 {audit['hashes']['candidate_tree_sha256']}")
    print("CANDIDATE_MATCHES_STAGE1_RETAINED_WORKSPACE true")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(p for p in trace_root.rglob("*") if p.is_file())
    assert len(trace_files) == 1
    trace_file = trace_files[0]
    trace_relative = trace_file.relative_to(trace_root).as_posix()
    trace_file_hash = sha256_file(trace_file)
    expected_trace_file_hash = result["outputs"]["evidence"][
        f"codex-trace/{trace_relative}"
    ]
    assert trace_file_hash == expected_trace_file_hash

    trace_digest = pipeline_content_tree_sha256(trace_root)
    usage_doc = json.loads(usage.read_text())
    assert trace_digest == usage_doc["source_trace_sha256"]
    print(f"TRACE_FILE_HASH_MATCH {trace_file_hash} {trace_relative}")
    print(f"TRACE_PIPELINE_CONTENT_TREE_SHA256 {trace_digest}")
    print(f"AUDIT_RECORDED_TRACE_TREE_SHA256 {audit['hashes']['generation_codex_trace_sha256']}")

    trace_types: Counter[str] = Counter()
    response_types: Counter[str] = Counter()
    trace_lines = 0
    for trace_lines, line in enumerate(trace_file.open(), 1):
        record = json.loads(line)
        trace_types[record["type"]] += 1
        if record["type"] == "response_item":
            response_types[record["payload"]["type"]] += 1
    print(f"TRACE_JSON_LINES_PARSED {trace_lines}")
    print(f"TRACE_TYPES {dict(sorted(trace_types.items()))}")
    print(f"TRACE_RESPONSE_TYPES {dict(sorted(response_types.items()))}")

    output_text = Path("/generation-evidence/codex-output.log").read_text()
    last_text = Path("/generation-evidence/codex-last.txt").read_text()
    prompt_text = Path("/generation-evidence/prompt.txt").read_text()
    print(f"GENERATION_OUTPUT_LINES_READ {len(output_text.splitlines())}")
    print(f"GENERATION_LAST_LINES_READ {len(last_text.splitlines())}")
    print(f"GENERATION_PROMPT_LINES_READ {len(prompt_text.splitlines())}")
    assert "RESULT: KPROVE_PASSED" in output_text
    assert "RESULT: KPROVE_PASSED" in last_text
    print("UNTRUSTED_GENERATION_RESULT_MARKER_PRESENT true")

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in required_candidate:
        require_regular(Path("/candidate") / name)
        print(f"REQUIRED_CANDIDATE_ARTIFACT_OK {name}")


if __name__ == "__main__":
    main()
