#!/usr/bin/env python3
"""Independent read-only integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"not a real directory: {path}")


def tree_rows(root: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            rows.append(("file", rel, sha256_file(path)))
        elif stat.S_ISDIR(mode):
            rows.append(("dir", rel, "-"))
        elif stat.S_ISLNK(mode):
            rows.append(("symlink", rel, os.readlink(path)))
        else:
            rows.append(("other", rel, oct(mode)))
    return rows


def reviewer_tree_hash(rows: list[tuple[str, str, str]]) -> str:
    digest = hashlib.sha256()
    for kind, rel, value in rows:
        digest.update(kind.encode())
        digest.update(b"\0")
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(value.encode())
        digest.update(b"\n")
    return digest.hexdigest()


def check_record(
    path: Path, expected_hash: str | None, expected_kind: str = "file"
) -> None:
    if expected_kind == "file":
        require_regular(path)
        actual = sha256_file(path)
        if expected_hash is not None and actual != expected_hash:
            raise AssertionError(
                f"hash mismatch: {path}: expected {expected_hash}, got {actual}"
            )
        print(f"OK regular sha256={actual} path={path}")
    else:
        require_directory(path)
        rows = tree_rows(path)
        bad = [row for row in rows if row[0] not in ("file", "dir")]
        if bad:
            raise AssertionError(f"linked/unsupported entries in {path}: {bad}")
        print(
            "OK directory "
            f"entries={len(rows)} reviewer_tree_sha256={reviewer_tree_hash(rows)} "
            f"path={path}"
        )


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/provenance_check.py")
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    if audit["record_layout"] != "pipeline-v3":
        raise AssertionError(f"unexpected record_layout: {audit['record_layout']}")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise AssertionError(f"unexpected semantics_mode: {audit['semantics_mode']}")
    hashes = audit["hashes"]

    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    check_record(lock_path, hashes["audit_campaign_lock_sha256"])
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    if lock != audit["audit_campaign"]:
        raise AssertionError("campaign lock differs from audit_campaign block")
    print("OK campaign lock content equals audit_input.audit_campaign")

    records = [
        (Path("/run.json"), "run_manifest_sha256"),
        (Path("/task.json"), "task_manifest_sha256"),
        (Path("/generation-result.json"), "stage1_result_sha256"),
        (GENERATION / "invocation.json", "stage1_invocation_sha256"),
        (GENERATION / "metrics.json", "generation_metrics_sha256"),
        (GENERATION / "runtime-metrics.json", "generation_runtime_metrics_sha256"),
        (GENERATION / "usage.json", "generation_usage_sha256"),
        (GENERATION / "codex-last.txt", "generation_codex_last_sha256"),
        (GENERATION / "codex-output.log", "generation_codex_output_sha256"),
        (GENERATION / "prompt.txt", "generation_prompt_sha256"),
        (REFERENCE / "canonical.py", "canonical_sha256"),
        (REFERENCE / "prompt.py", "trusted_prompt_sha256"),
        (REFERENCE / "py2mpy.py", "trusted_translator_sha256"),
        (CANDIDATE / "prompt.py", "candidate_prompt_sha256"),
        (CANDIDATE / "py2mpy.py", "candidate_translator_sha256"),
    ]
    for path, key in records:
        check_record(path, hashes[key])

    trace_root = GENERATION / "codex-trace"
    check_record(trace_root, None, "directory")
    trace_files = [path for path in trace_root.rglob("*") if path.is_file()]
    if len(trace_files) != 1:
        raise AssertionError(f"expected exactly one trace file, found {trace_files}")
    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    rel = trace_files[0].relative_to(GENERATION).as_posix()
    expected_trace_file_hash = result["outputs"]["evidence"].get(rel)
    check_record(trace_files[0], expected_trace_file_hash)
    line_count = 0
    with trace_files[0].open(encoding="utf-8") as stream:
        for line_count, line in enumerate(stream, 1):
            json.loads(line)
    print(f"OK structured trace JSON lines={line_count}")

    for required in (
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ):
        check_record(CANDIDATE / required, None)

    candidate_rows = tree_rows(CANDIDATE)
    candidate_bad = [
        row for row in candidate_rows if row[0] not in ("file", "dir")
    ]
    if candidate_bad:
        raise AssertionError(
            f"candidate tree contains linked/unsupported entries: {candidate_bad}"
        )
    print(
        "OK independently hashed complete candidate mount; "
        f"entries={len(candidate_rows)} "
        f"reviewer_tree_sha256={reviewer_tree_hash(candidate_rows)}"
    )

    if (CANDIDATE / "prompt.py").read_bytes() != (
        REFERENCE / "prompt.py"
    ).read_bytes():
        raise AssertionError("candidate prompt differs from trusted prompt")
    if (CANDIDATE / "py2mpy.py").read_bytes() != (
        REFERENCE / "py2mpy.py"
    ).read_bytes():
        raise AssertionError("candidate translator differs from trusted translator")
    print("OK candidate prompt and translator are byte-identical to trusted mounts")

    candidate_semantics = tree_rows(CANDIDATE / "reference-semantics")
    trusted_semantics = tree_rows(REFERENCE / "reference-semantics")
    if candidate_semantics != trusted_semantics:
        raise AssertionError("candidate supplied-semantics tree differs from trusted tree")
    if any(kind not in ("file", "dir") for kind, _, _ in candidate_semantics):
        raise AssertionError("candidate supplied-semantics tree contains a link")
    print(
        "OK candidate supplied-semantics tree is exactly equal by "
        f"path/type/content; entries={len(candidate_semantics)} "
        f"reviewer_tree_sha256={reviewer_tree_hash(candidate_semantics)}"
    )
    print("STAGE1_INFRASTRUCTURE_INTEGRITY=PASS")


if __name__ == "__main__":
    main()
