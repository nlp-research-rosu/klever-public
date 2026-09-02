#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit records."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-v3 tree algorithm recovered from the mounted runner source."""
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
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    assert os.access(path, os.R_OK), f"unreadable file: {path}"


def require_tree(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    assert os.access(path, os.R_OK | os.X_OK), f"unreadable directory: {path}"
    # sha256_tree also rejects every linked or unsupported descendant.
    sha256_tree(path)


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    assert actual == expected, f"{label}: expected {expected}, got {actual}"
    print(f"OK hash {label} {actual} {path}")


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    print("OK declared layout legacy-selected-stage1")
    print("OK declared semantics mode GENERATED_SEMANTICS")

    required_files = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
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
    ]
    for value in audit["container_paths"].values():
        path = Path(value)
        (require_tree if path.is_dir() else require_regular)(path)
        print(f"OK launcher mount type/readability {path}")
    for path in required_files:
        require_regular(path)
        print(f"OK required record {path}")
    for path in required_dirs:
        require_tree(path)
        print(f"OK required tree {path}")

    campaign_path = Path(audit["container_paths"]["audit_campaign_lock"])
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    assert campaign == audit["audit_campaign"], "campaign block differs from lock"
    check_hash(
        "audit_campaign_lock_sha256",
        campaign_path,
        audit["hashes"]["audit_campaign_lock_sha256"],
    )
    print("OK campaign JSON equals audit-input campaign block")

    hash_paths = {
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path(
            "/generation-evidence/invocation.json"
        ),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    }
    for label, path in hash_paths.items():
        check_hash(label, path, audit["hashes"][label])

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("OK candidate prompt byte-identical to trusted prompt")
    print("OK candidate translator byte-identical to trusted translator")

    assert not Path("/reference/reference-semantics").exists()
    assert audit["mount_reference_semantics"] is False
    assert audit["reference_semantics"] is None
    assert audit["hashes"]["trusted_reference_semantics_sha256"] is None
    assert audit["hashes"]["candidate_reference_semantics_sha256"] is None
    print("OK generated-semantics boundary: no trusted semantics mount")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    candidate_pipeline_hash = sha256_tree(Path("/candidate"))
    trace_pipeline_hash = sha256_tree(
        Path("/generation-evidence/codex-trace")
    )
    expected_workspace = result["outputs"]["workspace_sha256"]
    assert candidate_pipeline_hash == expected_workspace
    assert (
        candidate_pipeline_hash
        == invocation["outputs"]["workspace_sha256"]
        == invocation["retained_workspace_sha256"]
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    assert trace_pipeline_hash == usage["source_trace_sha256"]
    print(f"OK candidate pipeline tree hash {candidate_pipeline_hash}")
    print(f"OK trace pipeline tree hash {trace_pipeline_hash}")
    print(
        "RECORDED launcher candidate_tree_sha256 "
        + audit["hashes"]["candidate_tree_sha256"]
    )
    print(
        "RECORDED launcher generation_codex_trace_sha256 "
        + audit["hashes"]["generation_codex_trace_sha256"]
    )

    evidence_hashes = result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, f"generation-result evidence mismatch: {path}"
        print(f"OK result evidence hash {actual} {path}")

    proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in proof_artifacts:
        require_regular(Path("/candidate") / name)
        print(f"OK candidate proof artifact /candidate/{name}")

    print("INTEGRITY CHECKS PASSED")


if __name__ == "__main__":
    main()
