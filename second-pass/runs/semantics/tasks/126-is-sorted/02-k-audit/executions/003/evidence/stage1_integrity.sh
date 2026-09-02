#!/usr/bin/env bash
set -u

sha_file() {
  sha256sum "$1"
  printf 'status=%s command=sha256sum %s\n' "$?" "$1"
}

printf 'AUDIT INFRASTRUCTURE TYPES\n'
for path in \
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
  /reference/py2mpy.py \
  /reference/reference-semantics
do
  stat -c '%F | mode=%A | size=%s | %n' "$path"
  printf 'status=%s command=stat %s\n' "$?" "$path"
done

printf '\nRECORDED FILE HASH CHECKS\n'
for path in \
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
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T05-52-01-019f8e9a-8c6a-7f51-8b30-5aaf29584db0.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py
do
  sha_file "$path"
done

printf '\nCAMPAIGN JSON EQUALITY\n'
python3 - <<'PY'
import json
with open("/audit-input.json", encoding="utf-8") as handle:
    audit_input = json.load(handle)
with open("/audit-campaign-lock.json", encoding="utf-8") as handle:
    lock = json.load(handle)
print("campaign_equal=", audit_input["audit_campaign"] == lock)
raise SystemExit(0 if audit_input["audit_campaign"] == lock else 1)
PY
printf 'status=%s command=compare audit_campaign JSON to lock JSON\n' "$?"

printf '\nCANDIDATE/TRUSTED FIXED INPUT IDENTITY\n'
cmp -s /candidate/prompt.py /reference/prompt.py
printf 'status=%s command=cmp candidate/prompt.py reference/prompt.py\n' "$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'status=%s command=cmp candidate/py2mpy.py reference/py2mpy.py\n' "$?"
diff -r /candidate/reference-semantics /reference/reference-semantics
printf 'status=%s command=diff -r candidate/reference-semantics reference/reference-semantics\n' "$?"

printf '\nSYMLINK CHECKS\n'
find /candidate/reference-semantics /reference/reference-semantics -type l -printf '%p -> %l\n'
printf 'status=%s command=find supplied semantics trees -type l\n' "$?"

printf '\nPER-ENTRY SUPPLIED-SEMANTICS MANIFEST\n'
find /reference/reference-semantics -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum
printf 'status=%s command=sorted per-file sha256 trusted supplied semantics\n' "$?"
