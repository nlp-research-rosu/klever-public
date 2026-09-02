#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

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


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in sorted(dirnames + filenames):
            path = base / name
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries[relative] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                entries[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                entries[relative] = ("file", sha256_file(path))
            else:
                entries[relative] = ("other", None)
    return entries


def sha256_tree(root: Path) -> str:
    """Launcher-compatible tree digest, independently reimplemented here."""
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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
    manifest = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    task = json.loads(Path("/task.json").read_text())
    generation_result = json.loads(Path("/generation-result.json").read_text())
    expected_hashes = manifest["hashes"]
    paths = manifest["container_paths"]

    print(f"record_layout={manifest['record_layout']}")
    print(f"semantics_mode={manifest['semantics_mode']}")
    print(f"campaign_object_equal={manifest['audit_campaign'] == lock}")

    direct = {
        "audit_campaign_lock_sha256": Path(paths["audit_campaign_lock"]),
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    direct_ok = True
    for key, path in direct.items():
        exists = path.is_file() and not path.is_symlink()
        actual = sha256_file(path) if exists else "MISSING_OR_WRONG_TYPE"
        expected = expected_hashes[key]
        match = exists and actual == expected
        direct_ok &= match
        print(f"{key}: match={match} actual={actual} expected={expected} path={path}")

    trace_root = Path(paths["generation_trace"])
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    print(f"trace_jsonl_count={len(trace_files)}")
    for path in trace_files:
        print(f"trace_file={path} sha256={sha256_file(path)} size={path.stat().st_size}")

    # These are the pipeline-contract tree hashes.  The audit launcher also
    # records separately named copy/seal hashes (without "manifest" in the
    # semantics key); those use a different, launcher-private representation
    # and therefore must not be compared to this digest.
    tree_checks = {
        "candidate_pipeline_tree": (
            Path(paths["candidate"]), generation_result["outputs"]["workspace_sha256"]
        ),
        "candidate_semantics_manifest_tree": (
            Path(paths["candidate"]) / "reference-semantics",
            task["inputs"]["reference_semantics_sha256"],
        ),
        "trusted_semantics_manifest_tree": (
            Path("/reference/reference-semantics"),
            expected_hashes["trusted_reference_semantics_manifest_sha256"],
        ),
    }
    tree_ok = True
    for key, (path, expected) in tree_checks.items():
        actual = sha256_tree(path)
        match = actual == expected
        tree_ok &= match
        print(f"{key}: match={match} actual={actual} expected={expected} path={path}")

    print("launcher_seal_hashes_recorded_only=")
    for key in (
        "candidate_tree_sha256",
        "candidate_reference_semantics_sha256",
        "trusted_reference_semantics_sha256",
        "generation_codex_trace_sha256",
    ):
        print(f"  {key}={expected_hashes[key]}")

    required = [
        Path("/audit-input.json"), Path("/audit-campaign-lock.json"),
        Path("/run.json"), Path("/task.json"), Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"), trace_root,
        Path(paths["candidate"]), Path(paths["canonical"]),
        Path(paths["trusted_prompt"]), Path(paths["translator"]),
        Path("/reference/reference-semantics"),
    ]
    required_ok = True
    for path in required:
        ok = path.exists() and not path.is_symlink()
        required_ok &= ok
        print(f"required path={path} present_non_symlink={ok}")

    candidate = Path(paths["candidate"])
    candidate_links = [p for p in candidate.rglob("*") if p.is_symlink()]
    reference_links = [p for p in Path("/reference").rglob("*") if p.is_symlink()]
    generation_links = [p for p in Path("/generation-evidence").rglob("*") if p.is_symlink()]
    print(f"candidate_symlinks={candidate_links}")
    print(f"reference_symlinks={reference_links}")
    print(f"generation_symlinks={generation_links}")

    comparisons = [
        (candidate / "prompt.py", Path(paths["trusted_prompt"]), "prompt"),
        (candidate / "py2mpy.py", Path(paths["translator"]), "translator"),
    ]
    copy_ok = True
    for left, right, label in comparisons:
        same = (
            left.is_file() and right.is_file()
            and not left.is_symlink() and not right.is_symlink()
            and sha256_file(left) == sha256_file(right)
        )
        copy_ok &= same
        print(f"{label}_byte_identical={same}")

    candidate_semantics = tree_entries(candidate / "reference-semantics")
    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    semantics_equal = candidate_semantics == trusted_semantics
    print(f"semantics_entry_count_candidate={len(candidate_semantics)}")
    print(f"semantics_entry_count_trusted={len(trusted_semantics)}")
    print(f"semantics_tree_exact={semantics_equal}")
    if not semantics_equal:
        all_names = sorted(set(candidate_semantics) | set(trusted_semantics))
        for name in all_names:
            if candidate_semantics.get(name) != trusted_semantics.get(name):
                print(f"semantics_difference {name}: candidate={candidate_semantics.get(name)} trusted={trusted_semantics.get(name)}")

    print(
        "OVERALL="
        + ("PASS" if direct_ok and tree_ok and required_ok and copy_ok and semantics_equal
           and manifest["audit_campaign"] == lock and not candidate_links
           and not reference_links and not generation_links else "FAIL")
    )


if __name__ == "__main__":
    main()
