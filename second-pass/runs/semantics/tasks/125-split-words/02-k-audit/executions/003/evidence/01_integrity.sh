#!/usr/bin/env bash
set -u
set -o pipefail

echo '$ sha256sum launcher and required generation records'
sha256sum \
  /audit-input.json \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T05-48-35-019f8e97-685a-7650-9748-87cd7875d41f.jsonl
echo "sha256sum_exit=$?"

echo '$ compare campaign lock to audit-input audit_campaign and recompute lock hash'
python3 - <<'PY'
import hashlib
import json

with open("/audit-input.json", encoding="utf-8") as stream:
    audit_input = json.load(stream)
with open("/audit-campaign-lock.json", encoding="utf-8") as stream:
    lock = json.load(stream)
with open("/audit-campaign-lock.json", "rb") as stream:
    lock_hash = hashlib.sha256(stream.read()).hexdigest()

print("campaign_equal=", audit_input["audit_campaign"] == lock, sep="")
print("lock_hash=", lock_hash, sep="")
print("recorded_lock_hash=", audit_input["hashes"]["audit_campaign_lock_sha256"], sep="")
print("record_layout=", audit_input["record_layout"], sep="")
print("semantics_mode=", audit_input["semantics_mode"], sep="")
PY
echo "campaign_compare_exit=$?"

echo '$ cmp candidate prompt and translator against trusted mounts'
cmp /candidate/prompt.py /reference/prompt.py
echo "prompt_cmp_exit=$?"
cmp /candidate/py2mpy.py /reference/py2mpy.py
echo "translator_cmp_exit=$?"

echo '$ recursively compare supplied semantics and list symlinks'
diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
echo "semantics_diff_exit=$?"
find /candidate/reference-semantics /reference/reference-semantics -type l -print
echo "semantics_symlink_scan_exit=$?"

echo '$ enumerate mounted artifact types'
find \
  /candidate \
  /reference \
  /generation-evidence \
  -printf '%y %p -> %l\n' |
  sort
echo "mounted_type_inventory_exit=$?"

echo '$ independently hash every candidate file and hash the sorted manifest'
find /candidate -type f -print0 |
  sort -z |
  xargs -0 sha256sum |
  tee /tmp/audit-work/125-split-words/candidate-file-hashes.txt
echo "candidate_file_hashes_exit=$?"
sha256sum /tmp/audit-work/125-split-words/candidate-file-hashes.txt
echo "candidate_hash_manifest_exit=$?"
