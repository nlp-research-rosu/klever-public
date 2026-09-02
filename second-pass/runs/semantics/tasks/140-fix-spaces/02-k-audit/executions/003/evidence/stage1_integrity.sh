#!/usr/bin/env bash
set -u

echo '$ sha256sum launcher and provenance records'
sha256sum \
  /audit-input.json \
  /audit-campaign-lock.json \
  /audit-prompt.md \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T06-51-52-019f8ed1-593f-7043-8052-4f7d9771884d.jsonl
echo "exit=$?"

echo '$ python3: compare audit_campaign object with campaign-lock and verify recorded direct-file hashes'
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print("campaign_object_equal=", audit["audit_campaign"] == lock)
actual_lock = hashlib.sha256(Path("/audit-campaign-lock.json").read_bytes()).hexdigest()
print("campaign_lock_recorded=", audit["hashes"]["audit_campaign_lock_sha256"])
print("campaign_lock_actual=", actual_lock)
checks = {
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
failures = 0
for key, file_name in checks.items():
    actual = hashlib.sha256(Path(file_name).read_bytes()).hexdigest()
    expected = audit["hashes"][key]
    ok = actual == expected
    failures += not ok
    print(f"{key}: ok={ok} expected={expected} actual={actual} path={file_name}")
print("direct_hash_failures=", failures)
raise SystemExit(1 if failures or audit["audit_campaign"] != lock or actual_lock != audit["hashes"]["audit_campaign_lock_sha256"] else 0)
PY
echo "exit=$?"

echo '$ cmp trusted prompt and candidate prompt'
cmp /reference/prompt.py /candidate/prompt.py
echo "exit=$?"

echo '$ cmp trusted translator and candidate translator'
cmp /reference/py2mpy.py /candidate/py2mpy.py
echo "exit=$?"

echo '$ diff recursively, without dereferencing, trusted and candidate supplied semantics'
diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
echo "exit=$?"

echo '$ enumerate candidate semantics entries and types'
find /candidate/reference-semantics -printf '%y %m %s %P -> %l\n' | LC_ALL=C sort
echo "exit=$?"

echo '$ enumerate trusted semantics entries and types'
find /reference/reference-semantics -printf '%y %m %s %P -> %l\n' | LC_ALL=C sort
echo "exit=$?"

echo '$ search all protected input trees for symlinks'
find /candidate /reference /generation-evidence -type l -printf '%p -> %l\n' | LC_ALL=C sort
echo "exit=$?"

echo '$ parse every record in the structured generation trace'
python3 /audit-output/evidence/trace_summary.py \
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T06-51-52-019f8ed1-593f-7043-8052-4f7d9771884d.jsonl
echo "exit=$?"
