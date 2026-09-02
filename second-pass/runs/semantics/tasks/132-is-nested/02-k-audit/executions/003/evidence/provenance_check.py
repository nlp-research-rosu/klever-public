#!/usr/bin/env python3
"""Independent, read-only provenance and supplied-semantics integrity checker."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


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
    return "special"


def tree(root: Path) -> dict[str, dict[str, str | int]]:
    entries: dict[str, dict[str, str | int]] = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            entry: dict[str, str | int] = {
                "kind": kind(path),
                "mode": stat.S_IMODE(path.lstat().st_mode),
            }
            if entry["kind"] == "file":
                entry["sha256"] = sha256(path)
                entry["size"] = path.stat().st_size
            elif entry["kind"] == "symlink":
                entry["target"] = os.readlink(path)
            entries[rel] = entry
    return entries


def deterministic_tree_hash(entries: dict[str, dict[str, str | int]]) -> str:
    encoded = json.dumps(
        entries, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def recorded_workspace_tree_hash(root: Path) -> str:
    """Reimplement the pipeline-v2 workspace tree hash from mounted bytes."""
    entries: list[tuple[str, str, Path]] = []
    for base, dirs, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in dirs + files:
            path = base_path / name
            entry_kind = kind(path)
            if entry_kind not in {"file", "dir"}:
                raise AssertionError(f"unsupported tree entry: {path} ({entry_kind})")
            entries.append((path.relative_to(root).as_posix(), entry_kind, path))
    digest = hashlib.sha256()
    for relative, entry_kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(
            ("directory" if entry_kind == "dir" else "file").encode() + b"\0"
        )
        if entry_kind == "file":
            digest.update(path.stat().st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS {message}")


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())

require(audit["record_layout"] == "legacy-selected-stage1", "record layout")
require(audit["semantics_mode"] == "SUPPLIED_SEMANTICS", "semantics mode")
require(audit["audit_campaign"] == lock, "campaign lock equals audit campaign block")

paths = {
    "audit_campaign_lock": Path("/audit-campaign-lock.json"),
    "candidate": Path("/candidate"),
    "canonical": Path("/reference/canonical.py"),
    "generation_last": Path("/generation-evidence/codex-last.txt"),
    "generation_manifest": Path("/generation-evidence/invocation.json"),
    "generation_metrics": Path("/generation-evidence/metrics.json"),
    "generation_output": Path("/generation-evidence/codex-output.log"),
    "generation_root": Path("/generation-evidence"),
    "generation_trace": Path("/generation-evidence/codex-trace"),
    "run_manifest": Path("/run.json"),
    "stage1_result": Path("/generation-result.json"),
    "task_manifest": Path("/task.json"),
    "translator": Path("/reference/py2mpy.py"),
    "trusted_prompt": Path("/reference/prompt.py"),
}
require(audit["container_paths"] == {k: str(v) for k, v in paths.items()},
        "container_paths map")

for name, path in paths.items():
    require(path.exists() and os.access(path, os.R_OK), f"{name} readable at {path}")
    require(not path.is_symlink(), f"{name} is not a symlink")

required_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_records:
    require(path.exists() and os.access(path, os.R_OK), f"required record {path}")

direct_hashes = {
    "audit_campaign_lock_sha256": LOCK,
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "run_manifest_sha256": Path("/run.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "task_manifest_sha256": Path("/task.json"),
}
for key, path in direct_hashes.items():
    observed = sha256(path)
    require(observed == audit["hashes"][key], f"{key} = {observed}")

require(Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes(),
        "candidate prompt byte-identical to trusted prompt")
require(Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes(),
        "candidate translator byte-identical to trusted translator")

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = Path("/candidate/reference-semantics")
require(trusted_semantics.is_dir(), "trusted supplied-semantics mount exists")
require(candidate_semantics.is_dir(), "candidate supplied-semantics tree exists")
trusted_tree = tree(trusted_semantics)
candidate_tree = tree(candidate_semantics)
require(all(e["kind"] in {"file", "dir"} for e in trusted_tree.values()),
        "trusted semantics contains only regular files and directories")
require(all(e["kind"] in {"file", "dir"} for e in candidate_tree.values()),
        "candidate semantics contains only regular files and directories")
require(trusted_tree == candidate_tree,
        "candidate supplied-semantics tree exactly matches trusted tree")
print("INFO trusted semantics entries", len(trusted_tree))
print("INFO independent trusted semantics tree hash",
      deterministic_tree_hash(trusted_tree))
print("INFO independent candidate semantics tree hash",
      deterministic_tree_hash(candidate_tree))
semantics_workspace_hash = recorded_workspace_tree_hash(trusted_semantics)
require(
    semantics_workspace_hash
    == audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    f"trusted semantics workspace tree hash = {semantics_workspace_hash}",
)
require(
    recorded_workspace_tree_hash(candidate_semantics) == semantics_workspace_hash,
    "candidate semantics workspace tree hash equals trusted tree",
)

whole_candidate_tree = tree(Path("/candidate"))
require(
    all(e["kind"] in {"file", "dir"} for e in whole_candidate_tree.values()),
    "whole candidate tree contains only regular files and directories",
)
candidate_workspace_hash = recorded_workspace_tree_hash(Path("/candidate"))
result_workspace_hash = json.loads(
    Path("/generation-result.json").read_text()
)["outputs"]["workspace_sha256"]
require(
    candidate_workspace_hash == result_workspace_hash,
    f"candidate workspace tree hash = {candidate_workspace_hash}",
)
print("INFO independent whole-candidate manifest hash",
      deterministic_tree_hash(whole_candidate_tree))

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / rel
    require(path.is_file() and not path.is_symlink(), f"recorded evidence file {rel}")
    require(sha256(path) == expected, f"generation-result hash for {rel}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [p for p in trace_files if p.is_file()]
require(len(trace_files) == 1, "exactly one structured trace file")
trace_lines = 0
for trace_path in trace_files:
    with trace_path.open() as stream:
        for trace_lines, line in enumerate(stream, 1):
            json.loads(line)
require(trace_lines == 695, "structured trace has 695 valid JSONL records")
trace_workspace_hash = recorded_workspace_tree_hash(
    Path("/generation-evidence/codex-trace")
)
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
require(
    trace_workspace_hash == usage["source_trace_sha256"],
    f"structured-trace workspace tree hash = {trace_workspace_hash}",
)

print("RESULT provenance and supplied-semantics integrity checks passed")
