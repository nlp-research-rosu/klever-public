#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run stat -c '%F %a %U:%G %s %n -> %N' \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace \
  /candidate \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py

run sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/legacy-metrics.json \
  /generation-evidence/legacy-run-input.json \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T07-26-43-019f89ca-e5fc-7482-b894-6e10d45410ce.jsonl

run find /candidate /reference /generation-evidence -xdev \
  -printf '%y %m %u:%g %s %p -> %l\n'

run find /candidate /reference /generation-evidence -xdev -type l -print

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run test ! -e /reference/reference-semantics

run python3 -c '
import hashlib, json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print("campaign_block_equal:", audit["audit_campaign"] == lock)
print("campaign_lock_hash_equal:",
      hashlib.sha256(Path("/audit-campaign-lock.json").read_bytes()).hexdigest()
      == audit["hashes"]["audit_campaign_lock_sha256"])

paths = audit["container_paths"]
for key, value in sorted(paths.items()):
    path = Path(value)
    print("container_path", key, value,
          "exists=", path.exists(),
          "readable=", path.exists() and path.stat() is not None,
          "symlink=", path.is_symlink())

checks = {
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
    "generation_usage_sha256": "/generation-evidence/usage.json",
}
for key, value in checks.items():
    actual = hashlib.sha256(Path(value).read_bytes()).hexdigest()
    print("recorded_hash", key, "match=", actual == audit["hashes"][key],
          "actual=", actual)

invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
for rel, expected in sorted(invocation["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    print("invocation_evidence", rel, "match=", actual == expected,
          "actual=", actual)

trace = Path("/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T07-26-43-019f89ca-e5fc-7482-b894-6e10d45410ce.jsonl")
count = 0
for count, line in enumerate(trace.open(), 1):
    json.loads(line)
print("structured_trace_json_lines:", count)
'
