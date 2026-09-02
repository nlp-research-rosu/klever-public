#!/usr/bin/env python3
"""Independent launcher-record and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlink: {path}"
    assert path.is_file(), f"not a regular file: {path}"


def tree(root: Path) -> dict[str, tuple[str, str]]:
    assert root.is_dir() and not root.is_symlink(), f"bad tree root: {root}"
    result: dict[str, tuple[str, str]] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        assert not path.is_symlink(), f"symlinked entry: {path}"
        if path.is_dir():
            result[rel] = ("directory", "")
        elif path.is_file():
            result[rel] = ("file", digest(path))
        else:
            raise AssertionError(f"unexpected filesystem entry: {path}")
    return result


audit = json.loads(AUDIT_INPUT.read_text())
assert audit["record_layout"] == "pipeline-v3"
assert audit["problem_id"] == "147-get-max-triples"
assert audit["condition"] == "kit-semantics"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

paths = audit["container_paths"]
hashes = audit["hashes"]
required_container_paths = {
    "audit_campaign_lock",
    "candidate",
    "canonical",
    "generation_last",
    "generation_manifest",
    "generation_metrics",
    "generation_output",
    "generation_root",
    "generation_trace",
    "run_manifest",
    "stage1_result",
    "task_manifest",
    "translator",
    "trusted_prompt",
}
assert required_container_paths <= paths.keys()

file_hash_checks = {
    "/audit-campaign-lock.json": hashes["audit_campaign_lock_sha256"],
    "/reference/canonical.py": hashes["canonical_sha256"],
    "/reference/prompt.py": hashes["trusted_prompt_sha256"],
    "/reference/py2mpy.py": hashes["trusted_translator_sha256"],
    "/candidate/prompt.py": hashes["candidate_prompt_sha256"],
    "/candidate/py2mpy.py": hashes["candidate_translator_sha256"],
    "/run.json": hashes["run_manifest_sha256"],
    "/task.json": hashes["task_manifest_sha256"],
    "/generation-result.json": hashes["stage1_result_sha256"],
    "/generation-evidence/invocation.json": hashes["stage1_invocation_sha256"],
    "/generation-evidence/metrics.json": hashes["generation_metrics_sha256"],
    "/generation-evidence/runtime-metrics.json": hashes[
        "generation_runtime_metrics_sha256"
    ],
    "/generation-evidence/usage.json": hashes["generation_usage_sha256"],
    "/generation-evidence/codex-last.txt": hashes["generation_codex_last_sha256"],
    "/generation-evidence/codex-output.log": hashes[
        "generation_codex_output_sha256"
    ],
    "/generation-evidence/prompt.txt": hashes["generation_prompt_sha256"],
}

for name, expected in file_hash_checks.items():
    path = Path(name)
    regular(path)
    actual = digest(path)
    assert actual == expected, (name, expected, actual)
    print(f"FILE OK {actual} {name}")

lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert lock == audit["audit_campaign"]
print("CAMPAIGN LOCK OK exact JSON-object match")

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    regular(path)
    actual = digest(path)
    assert actual == expected, (str(path), expected, actual)
    print(f"GENERATION EVIDENCE OK {actual} {path}")

trace_root = Path(paths["generation_trace"])
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_files = [entry for entry in trace_root.rglob("*") if entry.is_file()]
assert trace_files, "empty structured trace"
for path in trace_files:
    regular(path)
print(f"TRACE TREE OK regular_files={len(trace_files)}")

for required in (
    "/candidate/solution.py",
    "/candidate/solution.mpy",
    "/candidate/verification.k",
    "/candidate/spec.k",
    "/candidate/prove.sh",
    "/candidate/PROOF.md",
):
    regular(Path(required))
print("CANDIDATE REQUIRED PROOF ARTIFACTS OK")

assert Path("/reference/reference-semantics").is_dir()
trusted_semantics = tree(Path("/reference/reference-semantics"))
candidate_semantics = tree(Path("/candidate/reference-semantics"))
assert trusted_semantics == candidate_semantics
print(
    "SUPPLIED SEMANTICS TREE OK "
    f"entries={len(trusted_semantics)} recursive path/type/byte identity"
)

assert digest(Path("/reference/prompt.py")) == digest(Path("/candidate/prompt.py"))
assert digest(Path("/reference/py2mpy.py")) == digest(Path("/candidate/py2mpy.py"))
print("PROMPT AND TRANSLATOR OK byte-identical to trusted mounts")
print("INTEGRITY CHECK PASS")
