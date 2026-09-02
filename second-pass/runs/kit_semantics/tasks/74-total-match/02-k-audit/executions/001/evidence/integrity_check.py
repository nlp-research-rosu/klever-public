#!/usr/bin/env python3
"""Independent pipeline-v3 mount and hash checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_sha256(root: Path) -> str:
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
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
                raise AssertionError(f"linked/unsupported entry: {path}")
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
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a regular file: {path}")


def compare_trees(left: Path, right: Path) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        pending = [root]
        while pending:
            directory = pending.pop()
            for child in os.scandir(directory):
                path = Path(child.path)
                rel = path.relative_to(root).as_posix()
                mode = child.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    result[rel] = ("directory", None)
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    result[rel] = ("file", file_sha256(path))
                else:
                    result[rel] = ("unsupported", None)
        return result

    left_entries = entries(left)
    right_entries = entries(right)
    if left_entries != right_entries:
        left_only = sorted(left_entries.keys() - right_entries.keys())
        right_only = sorted(right_entries.keys() - left_entries.keys())
        changed = sorted(
            key
            for key in left_entries.keys() & right_entries.keys()
            if left_entries[key] != right_entries[key]
        )
        raise AssertionError(
            f"tree mismatch left_only={left_only} right_only={right_only} "
            f"changed={changed}"
        )


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    if audit["record_layout"] != "pipeline-v3":
        raise AssertionError("unexpected record layout")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise AssertionError("unexpected semantics mode")
    if audit["audit_campaign"] != lock:
        raise AssertionError("campaign block differs from lock JSON")

    paths = audit["container_paths"]
    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path("/generation-evidence/prompt.txt"),
        Path(paths["canonical"]),
        Path(paths["trusted_prompt"]),
        Path(paths["translator"]),
    ]
    for path in required:
        require_regular(path)

    trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
    trace_regular = [path for path in trace_files if path.is_file()]
    if not trace_regular:
        raise AssertionError("structured trace is empty")
    for path in trace_files:
        if path.is_symlink():
            raise AssertionError(f"trace symlink: {path}")
        if not (path.is_dir() or path.is_file()):
            raise AssertionError(f"unsupported trace entry: {path}")

    hashes = audit["hashes"]
    direct_checks = {
        LOCK: hashes["audit_campaign_lock_sha256"],
        Path(paths["canonical"]): hashes["canonical_sha256"],
        Path(paths["trusted_prompt"]): hashes["trusted_prompt_sha256"],
        Path(paths["translator"]): hashes["trusted_translator_sha256"],
        Path("/run.json"): hashes["run_manifest_sha256"],
        Path("/task.json"): hashes["task_manifest_sha256"],
        Path("/generation-result.json"): hashes["stage1_result_sha256"],
        Path(paths["generation_manifest"]): hashes["stage1_invocation_sha256"],
        Path(paths["generation_metrics"]): hashes["generation_metrics_sha256"],
        Path("/generation-evidence/runtime-metrics.json"):
            hashes["generation_runtime_metrics_sha256"],
        Path("/generation-evidence/usage.json"): hashes["generation_usage_sha256"],
        Path(paths["generation_last"]): hashes["generation_codex_last_sha256"],
        Path(paths["generation_output"]): hashes["generation_codex_output_sha256"],
        Path("/generation-evidence/prompt.txt"):
            hashes["generation_prompt_sha256"],
    }
    for path, expected in direct_checks.items():
        actual = file_sha256(path)
        print(f"file {path}: expected={expected} actual={actual}")
        if actual != expected:
            raise AssertionError(f"hash mismatch: {path}")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    for rel, expected in result["outputs"]["evidence"].items():
        path = Path(paths["generation_root"]) / rel
        actual = file_sha256(path)
        print(f"result evidence {rel}: expected={expected} actual={actual}")
        if actual != expected:
            raise AssertionError(f"result evidence mismatch: {rel}")
    for rel, expected in invocation["outputs"]["evidence"].items():
        path = Path(paths["generation_root"]) / rel
        actual = file_sha256(path)
        if actual != expected:
            raise AssertionError(f"invocation evidence mismatch: {rel}")

    trace_tree = tree_sha256(Path(paths["generation_trace"]))
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    expected_trace_tree = usage["source_trace_sha256"]
    print(
        "trace pipeline tree: "
        f"expected={expected_trace_tree} actual={trace_tree}"
    )
    if trace_tree != expected_trace_tree:
        raise AssertionError("trace pipeline tree hash mismatch")
    print(
        "audit-recorded trace composite (launcher algorithm not encoded in "
        f"record): {hashes['generation_codex_trace_sha256']}"
    )

    candidate_tree = tree_sha256(Path(paths["candidate"]))
    expected_workspace = result["outputs"]["workspace_sha256"]
    print(
        f"candidate pipeline tree: expected={expected_workspace} "
        f"actual={candidate_tree}"
    )
    if candidate_tree != expected_workspace:
        raise AssertionError("candidate workspace differs from generation result")
    print(
        "audit-recorded candidate composite (launcher algorithm not encoded in "
        f"record): {hashes['candidate_tree_sha256']}"
    )

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path(paths["candidate"]) / "reference-semantics"
    compare_trees(trusted_semantics, candidate_semantics)
    trusted_tree = tree_sha256(trusted_semantics)
    candidate_semantics_tree = tree_sha256(candidate_semantics)
    expected_tree = hashes["trusted_reference_semantics_manifest_sha256"]
    print(
        f"trusted semantics tree: expected={expected_tree} actual={trusted_tree}"
    )
    print(f"candidate semantics tree: actual={candidate_semantics_tree}")
    if trusted_tree != expected_tree or candidate_semantics_tree != expected_tree:
        raise AssertionError("supplied semantics digest mismatch")
    print(
        "audit-recorded candidate/trusted semantics composite (launcher "
        "algorithm not encoded in record): "
        f"{hashes['candidate_reference_semantics_sha256']}"
    )

    candidate_prompt = Path(paths["candidate"]) / "prompt.py"
    candidate_translator = Path(paths["candidate"]) / "py2mpy.py"
    if candidate_prompt.read_bytes() != Path(paths["trusted_prompt"]).read_bytes():
        raise AssertionError("candidate prompt differs from trusted prompt")
    if (
        candidate_translator.read_bytes()
        != Path(paths["translator"]).read_bytes()
    ):
        raise AssertionError("candidate translator differs from trusted translator")

    print(f"campaign_lock_fields_match=true fields={len(lock)}")
    print(f"required_regular_records={len(required)}")
    print(f"trace_regular_files={len(trace_regular)}")
    print("candidate_prompt_matches_trusted=true")
    print("candidate_translator_matches_trusted=true")
    print("candidate_semantics_matches_trusted=true")
    print("INTEGRITY_CHECK: PASS")


if __name__ == "__main__":
    main()
