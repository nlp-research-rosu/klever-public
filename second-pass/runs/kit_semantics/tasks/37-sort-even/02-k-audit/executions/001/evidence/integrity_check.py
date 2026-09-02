#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required regular file has wrong type: {path}")
    if not os.access(path, os.R_OK):
        raise AssertionError(f"required file is unreadable: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"required directory has wrong type: {path}")
    if not os.access(path, os.R_OK | os.X_OK):
        raise AssertionError(f"required directory is unreadable: {path}")


def snapshot(root: Path) -> dict[str, tuple[str, str | None]]:
    """Return a path/type/content snapshot, rejecting all non-file/dir entries."""
    require_directory(root)
    result: dict[str, tuple[str, str | None]] = {}
    for parent, dirs, files in os.walk(root, topdown=True, followlinks=False):
        parent_path = Path(parent)
        for name in sorted(dirs + files):
            entry = parent_path / name
            relative = entry.relative_to(root).as_posix()
            mode = entry.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("dir", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256(entry))
            else:
                raise AssertionError(
                    f"forbidden non-file/dir entry ({stat.filemode(mode)}): {entry}"
                )
    return result


def snapshot_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    digest = hashlib.sha256()
    for relative, (kind, content_hash) in sorted(entries.items()):
        record = f"{kind}\\0{relative}\\0{content_hash or ''}\\n".encode()
        digest.update(record)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce the pipeline-v3 path/type/size/content tree digest."""
    require_directory(root)
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
                raise AssertionError(f"unsupported pipeline tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def check_hash(path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256(path)
    print(f"SHA256 {actual} {path}")
    if actual != expected:
        raise AssertionError(
            f"hash mismatch for {path}: expected {expected}, got {actual}"
        )


def main() -> int:
    require_regular(AUDIT_INPUT)
    data = json.loads(AUDIT_INPUT.read_text())
    if data["record_layout"] != "pipeline-v3":
        raise AssertionError(f"unexpected record layout: {data['record_layout']}")
    if data["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise AssertionError(f"unexpected semantics mode: {data['semantics_mode']}")

    paths = {key: Path(value) for key, value in data["container_paths"].items()}
    file_path_keys = {
        "audit_campaign_lock",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    }
    dir_path_keys = {"candidate", "generation_root", "generation_trace"}
    for key in sorted(file_path_keys):
        require_regular(paths[key])
        print(f"REQUIRED FILE OK {key} {paths[key]}")
    for key in sorted(dir_path_keys):
        require_directory(paths[key])
        print(f"REQUIRED DIR OK {key} {paths[key]}")

    required_pipeline_files = [
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required_pipeline_files:
        require_regular(path)
        print(f"PIPELINE-V3 RECORD OK {path}")

    trace_snapshot = snapshot(Path("/generation-evidence/codex-trace"))
    if not trace_snapshot:
        raise AssertionError("structured trace is empty")
    print(f"STRUCTURED TRACE ENTRIES {len(trace_snapshot)}")

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    if lock != data["audit_campaign"]:
        raise AssertionError("campaign lock JSON does not equal audit-input campaign block")
    print("CAMPAIGN LOCK BLOCK MATCH true")

    recorded = data["hashes"]
    file_hash_checks = {
        Path("/audit-campaign-lock.json"): recorded["audit_campaign_lock_sha256"],
        Path("/reference/canonical.py"): recorded["canonical_sha256"],
        Path("/reference/prompt.py"): recorded["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): recorded["trusted_translator_sha256"],
        Path("/candidate/prompt.py"): recorded["candidate_prompt_sha256"],
        Path("/candidate/py2mpy.py"): recorded["candidate_translator_sha256"],
        Path("/run.json"): recorded["run_manifest_sha256"],
        Path("/task.json"): recorded["task_manifest_sha256"],
        Path("/generation-result.json"): recorded["stage1_result_sha256"],
        Path("/generation-evidence/invocation.json"): recorded[
            "stage1_invocation_sha256"
        ],
        Path("/generation-evidence/metrics.json"): recorded[
            "generation_metrics_sha256"
        ],
        Path("/generation-evidence/runtime-metrics.json"): recorded[
            "generation_runtime_metrics_sha256"
        ],
        Path("/generation-evidence/usage.json"): recorded["generation_usage_sha256"],
        Path("/generation-evidence/codex-last.txt"): recorded[
            "generation_codex_last_sha256"
        ],
        Path("/generation-evidence/codex-output.log"): recorded[
            "generation_codex_output_sha256"
        ],
        Path("/generation-evidence/prompt.txt"): recorded["generation_prompt_sha256"],
    }
    for path, expected in file_hash_checks.items():
        check_hash(path, expected)

    trace_files = [
        path
        for path in Path("/generation-evidence/codex-trace").rglob("*")
        if path.is_file()
    ]
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    for record_name, record in [
        ("invocation", invocation["outputs"]["evidence"]),
        ("stage1-result", result["outputs"]["evidence"]),
    ]:
        for relative, expected in sorted(record.items()):
            path = Path("/generation-evidence") / relative
            check_hash(path, expected)
            print(f"{record_name.upper()} EVIDENCE HASH OK {relative}")

    if len(trace_files) != 1:
        raise AssertionError(f"expected one trace file, found {len(trace_files)}")
    # The launcher tree digest is path-aware and may use a different serialization.
    # This is an independent content digest over our explicit snapshot.
    print(
        "INDEPENDENT TRACE SNAPSHOT SHA256 "
        + snapshot_digest(trace_snapshot)
    )
    trace_pipeline_hash = pipeline_tree_digest(
        Path("/generation-evidence/codex-trace")
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    if trace_pipeline_hash != usage["source_trace_sha256"]:
        raise AssertionError("structured trace pipeline-tree digest mismatch")
    print(f"PIPELINE TRACE TREE SHA256 {trace_pipeline_hash}")

    if Path("/candidate/prompt.py").read_bytes() != Path(
        "/reference/prompt.py"
    ).read_bytes():
        raise AssertionError("candidate prompt differs from trusted prompt")
    if Path("/candidate/py2mpy.py").read_bytes() != Path(
        "/reference/py2mpy.py"
    ).read_bytes():
        raise AssertionError("candidate translator differs from trusted translator")
    print("CANDIDATE PROMPT BYTE MATCH true")
    print("CANDIDATE TRANSLATOR BYTE MATCH true")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_snapshot = snapshot(trusted_semantics)
    candidate_snapshot = snapshot(candidate_semantics)
    print(f"TRUSTED SEMANTICS ENTRIES {len(trusted_snapshot)}")
    print(f"CANDIDATE SEMANTICS ENTRIES {len(candidate_snapshot)}")
    print(
        "INDEPENDENT TRUSTED SEMANTICS SNAPSHOT SHA256 "
        + snapshot_digest(trusted_snapshot)
    )
    print(
        "INDEPENDENT CANDIDATE SEMANTICS SNAPSHOT SHA256 "
        + snapshot_digest(candidate_snapshot)
    )
    if trusted_snapshot != candidate_snapshot:
        all_paths = sorted(set(trusted_snapshot) | set(candidate_snapshot))
        differences = [
            path
            for path in all_paths
            if trusted_snapshot.get(path) != candidate_snapshot.get(path)
        ]
        raise AssertionError(
            "candidate supplied-semantics tree differs at: "
            + ", ".join(differences)
        )
    print("SUPPLIED SEMANTICS RECURSIVE TYPE/CONTENT MATCH true")

    trusted_semantics_pipeline_hash = pipeline_tree_digest(trusted_semantics)
    candidate_semantics_pipeline_hash = pipeline_tree_digest(candidate_semantics)
    expected_semantics_pipeline_hash = recorded[
        "trusted_reference_semantics_manifest_sha256"
    ]
    if trusted_semantics_pipeline_hash != expected_semantics_pipeline_hash:
        raise AssertionError("trusted semantics pipeline-tree digest mismatch")
    if candidate_semantics_pipeline_hash != expected_semantics_pipeline_hash:
        raise AssertionError("candidate semantics pipeline-tree digest mismatch")
    print(
        f"PIPELINE TRUSTED SEMANTICS TREE SHA256 "
        f"{trusted_semantics_pipeline_hash}"
    )
    print(
        f"PIPELINE CANDIDATE SEMANTICS TREE SHA256 "
        f"{candidate_semantics_pipeline_hash}"
    )

    task = json.loads(Path("/task.json").read_text())
    run = json.loads(Path("/run.json").read_text())
    if task["problem_id"] != data["problem_id"] or data["problem_id"] != "37-sort-even":
        raise AssertionError("problem-id mismatch")
    if task["condition"] != data["manifest"]["condition"]:
        raise AssertionError("condition mismatch")
    if run["run_id"] != data["run_id"]:
        raise AssertionError("run-id mismatch")
    if data["audit_campaign"] != lock:
        raise AssertionError("campaign mismatch")
    if (
        task["inputs"]["reference_semantics_sha256"]
        != trusted_semantics_pipeline_hash
    ):
        raise AssertionError("task semantics input digest mismatch")
    print("RUN/TASK/CONDITION CONSISTENCY true")

    required_candidate_artifacts = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    defects: list[str] = []
    for relative in required_candidate_artifacts:
        path = Path("/candidate") / relative
        try:
            require_regular(path)
        except (FileNotFoundError, AssertionError) as err:
            defects.append(str(err))
    if defects:
        print("CANDIDATE ARTIFACT DEFECTS")
        for defect in defects:
            print(defect)
    else:
        print("REQUIRED CANDIDATE PROOF ARTIFACTS PRESENT true")

    candidate_snapshot_all = snapshot(Path("/candidate"))
    print(
        "INDEPENDENT CANDIDATE SNAPSHOT SHA256 "
        + snapshot_digest(candidate_snapshot_all)
    )
    candidate_pipeline_hash = pipeline_tree_digest(Path("/candidate"))
    if candidate_pipeline_hash != invocation["outputs"]["workspace_sha256"]:
        raise AssertionError("candidate differs from invocation output workspace")
    if candidate_pipeline_hash != result["outputs"]["workspace_sha256"]:
        raise AssertionError("candidate differs from stage1 result workspace")
    print(f"PIPELINE CANDIDATE TREE SHA256 {candidate_pipeline_hash}")
    print(
        "LAUNCHER ALTERNATE CANDIDATE DIGEST RECORDED "
        + recorded["candidate_tree_sha256"]
    )
    print("INTEGRITY CHECK PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"INTEGRITY CHECK ERROR: {error}", file=sys.stderr)
        raise
