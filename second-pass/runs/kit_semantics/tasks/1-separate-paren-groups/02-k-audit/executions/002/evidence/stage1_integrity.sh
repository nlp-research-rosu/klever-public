#!/usr/bin/env bash
set -u

run_cmd() {
  local command_text="$1"
  printf '\n$ %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run_cmd "stat -c '%F %s %n' /audit-input.json /audit-campaign-lock.json /run.json /task.json /generation-result.json /generation-evidence/invocation.json /generation-evidence/metrics.json /generation-evidence/runtime-metrics.json /generation-evidence/usage.json /generation-evidence/codex-last.txt /generation-evidence/codex-output.log /generation-evidence/prompt.txt /generation-evidence/codex-trace /candidate /reference/canonical.py /reference/prompt.py /reference/py2mpy.py /reference/reference-semantics"
run_cmd "sha256sum /audit-campaign-lock.json /run.json /task.json /generation-result.json /generation-evidence/invocation.json /generation-evidence/metrics.json /generation-evidence/runtime-metrics.json /generation-evidence/usage.json /generation-evidence/codex-last.txt /generation-evidence/codex-output.log /generation-evidence/prompt.txt /generation-evidence/codex-trace/2026/07/24/rollout-2026-07-24T22-25-59-019f974e-ea3b-79b3-849b-474a773871f0.jsonl /reference/canonical.py /reference/prompt.py /reference/py2mpy.py /candidate/prompt.py /candidate/py2mpy.py"
run_cmd "python3 -c 'import json; a=json.load(open(\"/audit-input.json\")); b=json.load(open(\"/audit-campaign-lock.json\")); assert a[\"audit_campaign\"] == b; print(\"campaign block equals lock: yes\")'"
run_cmd "python3 -c 'import hashlib,json; a=json.load(open(\"/audit-input.json\")); d=hashlib.sha256(open(\"/audit-campaign-lock.json\",\"rb\").read()).hexdigest(); print(\"recorded\",a[\"hashes\"][\"audit_campaign_lock_sha256\"]); print(\"actual  \",d); assert d == a[\"hashes\"][\"audit_campaign_lock_sha256\"]'"
run_cmd "cmp -s /candidate/prompt.py /reference/prompt.py && echo 'candidate prompt byte-identical: yes'"
run_cmd "cmp -s /candidate/py2mpy.py /reference/py2mpy.py && echo 'candidate translator byte-identical: yes'"
run_cmd "diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics"
run_cmd "find -P /candidate/reference-semantics /reference/reference-semantics -printf '%y %P %s\\n' | sort"
run_cmd "find -P /candidate /generation-evidence /reference/reference-semantics -type l -printf '%p -> %l\\n'"
run_cmd "find -P /reference/reference-semantics -type f -printf '%P\\0' | sort -z | while IFS= read -r -d '' f; do sha256sum \"/reference/reference-semantics/\$f\"; done"
run_cmd "find -P /candidate/reference-semantics -type f -printf '%P\\0' | sort -z | while IFS= read -r -d '' f; do sha256sum \"/candidate/reference-semantics/\$f\"; done"
run_cmd "python3 /audit-output/evidence/trace_inventory.py"
run_cmd "wc -l /generation-evidence/codex-output.log /generation-evidence/codex-trace/2026/07/24/rollout-2026-07-24T22-25-59-019f974e-ea3b-79b3-849b-474a773871f0.jsonl"
run_cmd "rg -n 'RESULT:|#Top|WarnStuckClaimState|\\[Error\\]|kprove spec|kompile --backend|krun .*--definition|VALIDATED|SOUND-BUT-LIMITED|FORMALLY-SOUND-UNVALIDATED|Incomplete work' /generation-evidence/codex-output.log | sed -n '1,320p'"
