#!/usr/bin/env python3
"""Read-only integrity checks over launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, "/opt/humaneval/tools")
from pipeline_contract import sha256_tree  # type: ignore  # launcher helper


def load(path: str):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


audit = load("/audit-input.json")
lock = load("/audit-campaign-lock.json")
result = load("/generation-result.json")
invocation = load("/generation-evidence/invocation.json")

checks: list[tuple[str, bool, str]] = []


def check(label: str, actual, expected) -> None:
    checks.append((label, actual == expected, f"actual={actual!r} expected={expected!r}"))


check("campaign_block_equals_lock", audit["audit_campaign"], lock)
check(
    "audit_campaign_lock_sha256",
    sha256_file("/audit-campaign-lock.json"),
    audit["hashes"]["audit_campaign_lock_sha256"],
)

file_hashes = {
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
}
for key, path in file_hashes.items():
    check(key, sha256_file(path), audit["hashes"][key])

trace_relative = next(iter(result["outputs"]["evidence"]))
trace_relative = next(
    key for key in result["outputs"]["evidence"] if key.startswith("codex-trace/")
)
trace_path = "/generation-evidence/" + trace_relative
check(
    "trace_file_sha256_against_result",
    sha256_file(trace_path),
    result["outputs"]["evidence"][trace_relative],
)
check(
    "trace_file_sha256_against_invocation",
    sha256_file(trace_path),
    invocation["outputs"]["evidence"][trace_relative],
)
check(
    "pipeline_trace_tree_sha256",
    sha256_tree(Path("/generation-evidence/codex-trace")),
    load("/generation-evidence/usage.json")["source_trace_sha256"],
)
check(
    "pipeline_candidate_tree_sha256",
    sha256_tree(Path("/candidate")),
    result["outputs"]["workspace_sha256"],
)
check(
    "pipeline_candidate_tree_sha256_against_invocation",
    sha256_tree(Path("/candidate")),
    invocation["outputs"]["workspace_sha256"],
)
check(
    "candidate_prompt_byte_identity",
    Path("/candidate/prompt.py").read_bytes()
    == Path("/reference/prompt.py").read_bytes(),
    True,
)
check(
    "candidate_translator_byte_identity",
    Path("/candidate/py2mpy.py").read_bytes()
    == Path("/reference/py2mpy.py").read_bytes(),
    True,
)

required = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/usage.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    trace_path,
]
for path in required:
    mode = os.lstat(path).st_mode
    check(f"regular_file:{path}", stat.S_ISREG(mode), True)

candidate_required = [
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "loop-spec.k",
    "verified-lemma.k",
    "solution-program.k",
    "prove.sh",
    "prompt.py",
    "py2mpy.py",
]
for name in candidate_required:
    path = f"/candidate/{name}"
    mode = os.lstat(path).st_mode
    check(f"candidate_regular_file:{name}", stat.S_ISREG(mode), True)

unsupported_entries = []
for root, directories, files in os.walk("/candidate", followlinks=False):
    for name in directories + files:
        path = os.path.join(root, name)
        mode = os.lstat(path).st_mode
        if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            unsupported_entries.append(path)
check("candidate_has_no_symlink_or_special_entry", unsupported_entries, [])

check("reference_semantics_absent", os.path.lexists("/reference/reference-semantics"), False)

for label, passed, detail in checks:
    print(f"{'PASS' if passed else 'FAIL'} {label} {detail}")
print("audit_input_candidate_tree_digest=" + audit["hashes"]["candidate_tree_sha256"])
print("audit_input_trace_tree_digest=" + audit["hashes"]["generation_codex_trace_sha256"])
print("note=the two preceding launcher digests use a distinct audit-packaging tree scheme")
failures = sum(not passed for _, passed, _ in checks)
print(f"failure_count={failures}")
raise SystemExit(1 if failures else 0)
