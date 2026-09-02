#!/usr/bin/env python3
"""Independent launcher/mount integrity check for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hash(root: Path) -> str:
    """Hash path, kind, file size, and content; reject non-file/dir entries."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise ValueError(f"tree root is not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
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


def require_regular(path: Path, label: str, failures: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        failures.append(f"{label}: absent/unreadable: {error}")
        return
    if not stat.S_ISREG(mode):
        failures.append(f"{label}: expected real regular file, mode={oct(mode)}")
        return
    try:
        path.open("rb").close()
    except OSError as error:
        failures.append(f"{label}: unreadable: {error}")


def require_directory(path: Path, label: str, failures: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        failures.append(f"{label}: absent/unreadable: {error}")
        return
    if not stat.S_ISDIR(mode):
        failures.append(f"{label}: expected real directory, mode={oct(mode)}")
        return
    try:
        list(os.scandir(path))
    except OSError as error:
        failures.append(f"{label}: unreadable: {error}")


def check_equal(label: str, actual: object, expected: object, failures: list[str]) -> None:
    print(f"{label}: actual={actual!r} expected={expected!r}")
    if actual != expected:
        failures.append(f"{label}: mismatch")


def main() -> int:
    failures: list[str] = []
    require_regular(AUDIT_INPUT, "launcher audit input", failures)
    if failures:
        print("\n".join(failures))
        return 1
    document = json.loads(AUDIT_INPUT.read_text())
    paths = {key: Path(value) for key, value in document["container_paths"].items()}
    hashes = document["hashes"]

    check_equal("record layout", document["record_layout"], "legacy-selected-stage1", failures)
    check_equal("semantics mode", document["semantics_mode"], "GENERATED_SEMANTICS", failures)

    required_files = {
        "launcher audit input": AUDIT_INPUT,
        "campaign lock": paths["audit_campaign_lock"],
        "run manifest": paths["run_manifest"],
        "task manifest": paths["task_manifest"],
        "stage1 result": paths["stage1_result"],
        "stage1 invocation": paths["generation_manifest"],
        "generation metrics": paths["generation_metrics"],
        "generation last": paths["generation_last"],
        "generation output": paths["generation_output"],
        "generation prompt": paths["generation_root"] / "prompt.txt",
        "trusted canonical": paths["canonical"],
        "trusted prompt": paths["trusted_prompt"],
        "trusted translator": paths["translator"],
    }
    usage_path = paths["generation_root"] / "usage.json"
    if usage_path.exists():
        required_files["generation usage (present)"] = usage_path
    for label, path in required_files.items():
        require_regular(path, label, failures)
    required_directories = {
        "candidate mount": paths["candidate"],
        "generation root": paths["generation_root"],
        "generation trace": paths["generation_trace"],
    }
    for label, path in required_directories.items():
        require_directory(path, label, failures)

    if any("absent/unreadable" in item or "expected real" in item for item in failures):
        print("INFRASTRUCTURE_TYPE_OR_PRESENCE_FAILURES:")
        print("\n".join(failures))
        return 1

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    check_equal("campaign lock object", lock, document["audit_campaign"], failures)
    check_equal(
        "campaign lock SHA-256",
        file_hash(paths["audit_campaign_lock"]),
        hashes["audit_campaign_lock_sha256"],
        failures,
    )

    direct_hashes = {
        "canonical_sha256": paths["canonical"],
        "trusted_prompt_sha256": paths["trusted_prompt"],
        "trusted_translator_sha256": paths["translator"],
        "run_manifest_sha256": paths["run_manifest"],
        "task_manifest_sha256": paths["task_manifest"],
        "stage1_result_sha256": paths["stage1_result"],
        "stage1_invocation_sha256": paths["generation_manifest"],
        "generation_metrics_sha256": paths["generation_metrics"],
        "generation_codex_last_sha256": paths["generation_last"],
        "generation_codex_output_sha256": paths["generation_output"],
        "generation_prompt_sha256": paths["generation_root"] / "prompt.txt",
    }
    if usage_path.exists():
        direct_hashes["generation_usage_sha256"] = usage_path
    for key, path in direct_hashes.items():
        check_equal(key, file_hash(path), hashes[key], failures)

    # The legacy-selected launcher records its own opaque tree digests in
    # audit-input.  Independently reconstruct the documented pipeline-v3
    # content/size/path digest and bind it to the stage records that declare
    # that convention.  Also print the opaque launcher values for review.
    invocation = json.loads(paths["generation_manifest"].read_text())
    usage = json.loads(usage_path.read_text()) if usage_path.exists() else None
    independent_trace_tree_hash = tree_hash(paths["generation_trace"])
    independent_candidate_tree_hash = tree_hash(paths["candidate"])
    print(
        "audit-input opaque generation_codex_trace_sha256="
        f"{hashes['generation_codex_trace_sha256']!r}"
    )
    print(
        "audit-input opaque candidate_tree_sha256="
        f"{hashes['candidate_tree_sha256']!r}"
    )
    if usage is not None:
        check_equal(
            "independent trace tree versus usage source_trace_sha256",
            independent_trace_tree_hash,
            usage["source_trace_sha256"],
            failures,
        )
    check_equal(
        "independent candidate tree versus invocation retained workspace",
        independent_candidate_tree_hash,
        invocation["retained_workspace_sha256"],
        failures,
    )

    candidate_prompt = paths["candidate"] / "prompt.py"
    candidate_translator = paths["candidate"] / "py2mpy.py"
    require_regular(candidate_prompt, "candidate prompt", failures)
    require_regular(candidate_translator, "candidate translator", failures)
    if candidate_prompt.is_file():
        check_equal(
            "candidate_prompt_sha256",
            file_hash(candidate_prompt),
            hashes["candidate_prompt_sha256"],
            failures,
        )
        check_equal(
            "candidate prompt versus trusted",
            file_hash(candidate_prompt),
            file_hash(paths["trusted_prompt"]),
            failures,
        )
    if candidate_translator.is_file():
        check_equal(
            "candidate_translator_sha256",
            file_hash(candidate_translator),
            hashes["candidate_translator_sha256"],
            failures,
        )
        check_equal(
            "candidate translator versus trusted",
            file_hash(candidate_translator),
            file_hash(paths["translator"]),
            failures,
        )

    reference_semantics = Path("/reference/reference-semantics")
    candidate_reference_semantics = paths["candidate"] / "reference-semantics"
    check_equal("trusted reference semantics absent", reference_semantics.exists(), False, failures)
    check_equal(
        "candidate reference semantics absent",
        candidate_reference_semantics.exists(),
        False,
        failures,
    )
    check_equal("declared trusted semantics hash", hashes["trusted_reference_semantics_sha256"], None, failures)
    check_equal("declared candidate semantics hash", hashes["candidate_reference_semantics_sha256"], None, failures)

    task = json.loads(paths["task_manifest"].read_text())
    enriched_task = dict(task)
    enriched_task["config"] = document["manifest_config"]
    check_equal("embedded manifest versus launcher-enriched task manifest", document["manifest"], enriched_task, failures)
    check_equal("task problem", task["problem_id"], document["problem_id"], failures)
    check_equal("launcher manifest config", document["manifest_config"], document["config"], failures)

    result = json.loads(paths["stage1_result"].read_text())
    for relative, expected in invocation["outputs"]["evidence"].items():
        evidence_path = paths["generation_root"] / relative
        require_regular(evidence_path, f"invocation evidence {relative}", failures)
        if evidence_path.is_file():
            check_equal(
                f"invocation evidence hash {relative}",
                file_hash(evidence_path),
                expected,
                failures,
            )
    for relative, expected in result["outputs"]["evidence"].items():
        evidence_path = paths["generation_root"] / relative
        require_regular(evidence_path, f"result evidence {relative}", failures)
        if evidence_path.is_file():
            check_equal(
                f"result evidence hash {relative}",
                file_hash(evidence_path),
                expected,
                failures,
            )

    trace_files = sorted(paths["generation_trace"].rglob("*"))
    print("TRACE_ENTRIES:")
    for path in trace_files:
        kind = "dir" if path.is_dir() else "file" if path.is_file() else "unsupported"
        print(f"{kind} {path.relative_to(paths['generation_trace'])}")

    if failures:
        print("FAILURES:")
        print("\n".join(failures))
        return 1
    print("PROVENANCE_CHECK: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
