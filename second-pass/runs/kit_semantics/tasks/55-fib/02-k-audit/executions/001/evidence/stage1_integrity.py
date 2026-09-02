#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, "/opt/humaneval/tools")
from pipeline_contract import sha256_tree  # type: ignore  # noqa: E402


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")
    print(f"REGULAR {path} size={path.stat().st_size}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"not a real directory: {path}")
    print(f"DIRECTORY {path}")


def require_tree_nodes_regular(root: Path) -> None:
    for directory, directory_names, file_names in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in directory_names:
            require_directory(directory_path / name)
        for name in file_names:
            require_regular(directory_path / name)


audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
campaign_lock = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))
hashes = audit_input["hashes"]

assert audit_input["problem_id"] == "55-fib"
assert audit_input["condition"] == "kit-semantics"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit_input["record_layout"] == "pipeline-v3"
assert audit_input["mount_reference_semantics"] is True
assert audit_input["audit_campaign"] == campaign_lock
print("JSON campaign lock exactly equals audit-input audit_campaign block")

required_files = [
    AUDIT_INPUT,
    CAMPAIGN_LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
required_directories = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference/reference-semantics"),
]
for path in required_files:
    require_regular(path)
for path in required_directories:
    require_directory(path)
require_tree_nodes_regular(Path("/generation-evidence/codex-trace"))
require_tree_nodes_regular(Path("/reference/reference-semantics"))
require_tree_nodes_regular(Path("/candidate/reference-semantics"))

direct_expectations = {
    Path("/audit-campaign-lock.json"): hashes["audit_campaign_lock_sha256"],
    Path("/reference/canonical.py"): hashes["canonical_sha256"],
    Path("/reference/prompt.py"): hashes["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): hashes["trusted_translator_sha256"],
    Path("/candidate/prompt.py"): hashes["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): hashes["candidate_translator_sha256"],
    Path("/run.json"): hashes["run_manifest_sha256"],
    Path("/task.json"): hashes["task_manifest_sha256"],
    Path("/generation-result.json"): hashes["stage1_result_sha256"],
    Path("/generation-evidence/invocation.json"): hashes["stage1_invocation_sha256"],
    Path("/generation-evidence/metrics.json"): hashes["generation_metrics_sha256"],
    Path("/generation-evidence/runtime-metrics.json"): hashes[
        "generation_runtime_metrics_sha256"
    ],
    Path("/generation-evidence/usage.json"): hashes["generation_usage_sha256"],
    Path("/generation-evidence/codex-last.txt"): hashes[
        "generation_codex_last_sha256"
    ],
    Path("/generation-evidence/codex-output.log"): hashes[
        "generation_codex_output_sha256"
    ],
    Path("/generation-evidence/prompt.txt"): hashes["generation_prompt_sha256"],
}
for path, expected in direct_expectations.items():
    actual = file_sha256(path)
    assert actual == expected, (path, actual, expected)
    print(f"SHA256 MATCH {path} {actual}")

generation_result = json.loads(
    Path("/generation-result.json").read_text(encoding="utf-8")
)
task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
usage = json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)

candidate_tree = sha256_tree(Path("/candidate"))
assert candidate_tree == generation_result["outputs"]["workspace_sha256"]
assert candidate_tree == invocation["outputs"]["workspace_sha256"]
print(f"PIPELINE TREE MATCH /candidate {candidate_tree}")

candidate_semantics_tree = sha256_tree(Path("/candidate/reference-semantics"))
trusted_semantics_tree = sha256_tree(Path("/reference/reference-semantics"))
assert candidate_semantics_tree == trusted_semantics_tree
assert trusted_semantics_tree == task["inputs"]["reference_semantics_sha256"]
print(f"PIPELINE TREE MATCH supplied semantics {trusted_semantics_tree}")

trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
assert trace_tree == usage["source_trace_sha256"]
print(f"PIPELINE TREE MATCH generation trace {trace_tree}")

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print("BYTE MATCH candidate prompt/translator against trusted mounts")

candidate_entries = {}
trusted_entries = {}
for root, entries in (
    (Path("/candidate/reference-semantics"), candidate_entries),
    (Path("/reference/reference-semantics"), trusted_entries),
):
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            entries[relative] = ("directory", None)
        elif stat.S_ISREG(mode):
            entries[relative] = ("file", file_sha256(path))
        else:
            entries[relative] = ("unsupported", None)
assert candidate_entries == trusted_entries
print(
    "RECURSIVE ENTRY/TYPE/BYTE MATCH candidate/reference-semantics "
    f"entries={len(candidate_entries)}"
)

candidate_required = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for name in candidate_required:
    require_regular(Path("/candidate") / name)

print("STAGE1_INTEGRITY_OK")
