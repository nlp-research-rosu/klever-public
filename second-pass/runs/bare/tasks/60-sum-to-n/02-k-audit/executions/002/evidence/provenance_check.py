#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, "/opt/humaneval/tools")
import pipeline_contract  # type: ignore  # benchmark-provided digest implementation


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def require_tree(path: Path) -> None:
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise AssertionError(f"not a real directory: {path}")
    pending = [path]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            child = Path(entry.path)
            if stat.S_ISDIR(mode):
                pending.append(child)
            elif not stat.S_ISREG(mode):
                raise AssertionError(f"linked or unsupported tree entry: {child}")


def check_file(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256(path)
    status = "OK" if actual == expected else "MISMATCH"
    print(f"{label}: {status} actual={actual} expected={expected} path={path}")
    if actual != expected:
        raise AssertionError(f"{label} hash mismatch")


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    assert audit_input["record_layout"] == "legacy-selected-stage1"
    assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
    hashes = audit_input["hashes"]

    lock_path = Path(audit_input["container_paths"]["audit_campaign_lock"])
    require_regular(lock_path)
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    assert lock == audit_input["audit_campaign"]
    print("campaign block equals /audit-campaign-lock.json: OK")
    audit_prompt = Path("/audit-prompt.md")
    require_regular(audit_prompt)
    actual_audit_prompt_hash = sha256(audit_prompt)
    assert actual_audit_prompt_hash == lock["audit_prompt_sha256"]
    print(f"audit prompt matches campaign hash: OK digest={actual_audit_prompt_hash}")

    required_files = [
        AUDIT_INPUT,
        lock_path,
        Path(audit_input["container_paths"]["run_manifest"]),
        Path(audit_input["container_paths"]["task_manifest"]),
        Path(audit_input["container_paths"]["stage1_result"]),
        Path(audit_input["container_paths"]["generation_manifest"]),
        Path(audit_input["container_paths"]["generation_metrics"]),
        Path(audit_input["container_paths"]["generation_last"]),
        Path(audit_input["container_paths"]["generation_output"]),
        Path(audit_input["container_paths"]["generation_root"]) / "prompt.txt",
        Path(audit_input["container_paths"]["canonical"]),
        Path(audit_input["container_paths"]["trusted_prompt"]),
        Path(audit_input["container_paths"]["translator"]),
    ]
    usage = Path(audit_input["container_paths"]["generation_root"]) / "usage.json"
    if usage.exists():
        required_files.append(usage)
    for path in required_files:
        require_regular(path)
    require_tree(Path(audit_input["container_paths"]["candidate"]))
    require_tree(Path(audit_input["container_paths"]["generation_trace"]))
    print(f"required regular files readable: OK count={len(required_files)}")
    print("candidate and structured-trace trees contain only real files/directories: OK")

    checks = [
        ("audit_campaign_lock_sha256", lock_path),
        ("canonical_sha256", Path("/reference/canonical.py")),
        ("trusted_prompt_sha256", Path("/reference/prompt.py")),
        ("trusted_translator_sha256", Path("/reference/py2mpy.py")),
        ("candidate_prompt_sha256", Path("/candidate/prompt.py")),
        ("candidate_translator_sha256", Path("/candidate/py2mpy.py")),
        ("generation_codex_last_sha256", Path("/generation-evidence/codex-last.txt")),
        ("generation_codex_output_sha256", Path("/generation-evidence/codex-output.log")),
        ("generation_metrics_sha256", Path("/generation-evidence/metrics.json")),
        ("generation_prompt_sha256", Path("/generation-evidence/prompt.txt")),
        ("generation_usage_sha256", Path("/generation-evidence/usage.json")),
        ("run_manifest_sha256", Path("/run.json")),
        ("task_manifest_sha256", Path("/task.json")),
        ("stage1_result_sha256", Path("/generation-result.json")),
        ("stage1_invocation_sha256", Path("/generation-evidence/invocation.json")),
    ]
    for label, path in checks:
        check_file(label, path, hashes[label])

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("candidate prompt byte-identical to trusted prompt: OK")
    print("candidate translator byte-identical to trusted translator: OK")

    reference_semantics = Path("/reference/reference-semantics")
    assert not reference_semantics.exists() and not reference_semantics.is_symlink()
    print("generated-semantics boundary (no reference-semantics mount): OK")

    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    generation_result = json.loads(Path("/generation-result.json").read_text())
    candidate_pipeline_digest = pipeline_contract.sha256_tree(Path("/candidate"))
    assert candidate_pipeline_digest == invocation["retained_workspace_sha256"]
    assert candidate_pipeline_digest == invocation["outputs"]["workspace_sha256"]
    assert candidate_pipeline_digest == generation_result["outputs"]["workspace_sha256"]
    print(
        "candidate canonical tree digest matches invocation/result: OK "
        f"digest={candidate_pipeline_digest}"
    )

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert len(trace_files) == 1
    relative_trace = trace_files[0].relative_to("/generation-evidence").as_posix()
    trace_file_digest = sha256(trace_files[0])
    assert trace_file_digest == invocation["outputs"]["evidence"][relative_trace]
    assert trace_file_digest == generation_result["outputs"]["evidence"][relative_trace]
    print(f"structured trace file hash matches invocation/result: OK digest={trace_file_digest}")

    usage_document = json.loads(Path("/generation-evidence/usage.json").read_text())
    trace_tree_digest = pipeline_contract.sha256_tree(Path("/generation-evidence/codex-trace"))
    assert trace_tree_digest == usage_document["source_trace_sha256"]
    print(f"structured trace canonical tree digest matches usage record: OK digest={trace_tree_digest}")

    for record_name in ("invocation.json",):
        record = json.loads((Path("/generation-evidence") / record_name).read_text())
        for relative, expected in record["outputs"]["evidence"].items():
            check_file(
                f"{record_name}:outputs.evidence:{relative}",
                Path("/generation-evidence") / relative,
                expected,
            )
    result_record = json.loads(Path("/generation-result.json").read_text())
    for relative, expected in result_record["outputs"]["evidence"].items():
        check_file(
            f"generation-result:outputs.evidence:{relative}",
            Path("/generation-evidence") / relative,
            expected,
        )

    print(
        "launcher-recorded opaque mount digests (recorded for comparison): "
        f"candidate_tree_sha256={hashes['candidate_tree_sha256']} "
        f"generation_codex_trace_sha256={hashes['generation_codex_trace_sha256']}"
    )
    print("PROVENANCE_CHECK: PASS")


if __name__ == "__main__":
    main()
