#!/usr/bin/env python3
"""Independent integrity checks for the 49-modp audit mounts."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({stat.S_IFMT(mode):#o})"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            value = sha256(path) if entry_kind == "file" else None
            if entry_kind == "symlink":
                value = os.readlink(path)
            result[rel] = (entry_kind, value)
    return result


def check(condition: bool, description: str, failures: list[str]) -> None:
    print(("PASS " if condition else "FAIL ") + description)
    if not condition:
        failures.append(description)


def main() -> int:
    failures: list[str] = []
    manifest = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))

    check(manifest["record_layout"] == "legacy-selected-stage1",
          "record layout is legacy-selected-stage1", failures)
    check(manifest["semantics_mode"] == "SUPPLIED_SEMANTICS",
          "semantics mode is SUPPLIED_SEMANTICS", failures)

    campaign_path = Path(manifest["container_paths"]["audit_campaign_lock"])
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    check(campaign == manifest["audit_campaign"],
          "campaign lock JSON equals audit-input campaign block", failures)
    check(sha256(campaign_path) == manifest["hashes"]["audit_campaign_lock_sha256"],
          "campaign lock SHA-256 matches launcher record", failures)

    required_launcher_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
    ]
    for path in required_launcher_files:
        check(path.exists() and kind(path) == "file" and os.access(path, os.R_OK),
              f"required launcher record is a readable regular file: {path}",
              failures)

    trace_root = GENERATION / "codex-trace"
    trace_files = sorted(p for p in trace_root.rglob("*") if p.is_file())
    check(trace_root.exists() and kind(trace_root) == "dir",
          "structured trace root is a directory", failures)
    check(bool(trace_files), "structured trace contains at least one file", failures)
    for path in trace_root.rglob("*"):
        check(kind(path) in {"dir", "file"},
              f"trace entry is not a symlink/special file: {path}", failures)

    hash_paths = {
        "canonical_sha256": REFERENCE / "canonical.py",
        "trusted_prompt_sha256": REFERENCE / "prompt.py",
        "trusted_translator_sha256": REFERENCE / "py2mpy.py",
        "candidate_prompt_sha256": CANDIDATE / "prompt.py",
        "candidate_translator_sha256": CANDIDATE / "py2mpy.py",
        "generation_codex_last_sha256": GENERATION / "codex-last.txt",
        "generation_codex_output_sha256": GENERATION / "codex-output.log",
        "generation_metrics_sha256": GENERATION / "metrics.json",
        "generation_prompt_sha256": GENERATION / "prompt.txt",
        "generation_usage_sha256": GENERATION / "usage.json",
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_invocation_sha256": GENERATION / "invocation.json",
        "stage1_result_sha256": Path("/generation-result.json"),
    }
    for key, path in hash_paths.items():
        expected = manifest["hashes"][key]
        actual = sha256(path)
        check(actual == expected, f"{key}: {actual}", failures)

    check((CANDIDATE / "prompt.py").read_bytes()
          == (REFERENCE / "prompt.py").read_bytes(),
          "candidate prompt is byte-identical to trusted prompt", failures)
    check((CANDIDATE / "py2mpy.py").read_bytes()
          == (REFERENCE / "py2mpy.py").read_bytes(),
          "candidate translator is byte-identical to trusted translator", failures)

    trusted_semantics = REFERENCE / "reference-semantics"
    candidate_semantics = CANDIDATE / "reference-semantics"
    check(trusted_semantics.exists() and kind(trusted_semantics) == "dir",
          "trusted supplied-semantics tree is present", failures)
    trusted_tree = tree_entries(trusted_semantics)
    candidate_tree = tree_entries(candidate_semantics)
    check(candidate_tree == trusted_tree,
          "candidate supplied-semantics tree has exactly the trusted paths, "
          "types, link targets, and file bytes", failures)
    for rel, (entry_kind, digest) in sorted(candidate_tree.items()):
        print(f"SEMANTICS {entry_kind} {rel}"
              + (f" sha256={digest}" if digest is not None else ""))

    required_candidate_files = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for rel in required_candidate_files:
        path = CANDIDATE / rel
        check(path.exists() and kind(path) == "file" and path.stat().st_size > 0,
              f"required candidate proof artifact is a nonempty regular file: {rel}",
              failures)

    print(f"SUMMARY failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
