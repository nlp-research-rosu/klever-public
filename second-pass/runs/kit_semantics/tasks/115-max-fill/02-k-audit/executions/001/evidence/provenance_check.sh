#!/usr/bin/env bash
set -uo pipefail

status=0

check_regular() {
  local path="$1"
  if [[ ! -f "$path" || -L "$path" || ! -r "$path" ]]; then
    echo "BAD_REQUIRED_RECORD $path"
    status=1
  else
    echo "OK_REQUIRED_RECORD $path"
  fi
}

echo 'COMMAND: sha256sum launcher manifests, trusted inputs, candidate copies, and pipeline-v3 generation records'
sha256sum \
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
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/29/rollout-2026-07-29T11-33-15-019faeb9-1e01-7b50-b285-1e2fbaf855cb.jsonl \
  || status=1

echo 'COMMAND: require all launcher and pipeline-v3 records to be readable regular non-symlink files'
for path in \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/29/rollout-2026-07-29T11-33-15-019faeb9-1e01-7b50-b285-1e2fbaf855cb.jsonl
do
  check_regular "$path"
done

echo 'COMMAND: compare audit_campaign object with /audit-campaign-lock.json'
python3 -c 'import json,sys; a=json.load(open("/audit-input.json"))["audit_campaign"]; b=json.load(open("/audit-campaign-lock.json")); print("AUDIT_CAMPAIGN_MATCH", a == b); sys.exit(0 if a == b else 1)' \
  || status=1

echo 'COMMAND: cmp trusted prompt and translator against candidate copies'
cmp -s /reference/prompt.py /candidate/prompt.py
prompt_status=$?
echo "PROMPT_CMP_EXIT $prompt_status"
(( prompt_status == 0 )) || status=1
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
echo "TRANSLATOR_CMP_EXIT $translator_status"
(( translator_status == 0 )) || status=1

echo 'COMMAND: list any symlinks in all mounted provenance, trusted, and candidate trees'
find -P \
  /candidate \
  /reference \
  /generation-evidence \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  -type l -printf '%p -> %l\n' | sort

echo 'COMMAND: compare supplied-semantics entry names and filesystem types'
diff -u \
  <(find -P /reference/reference-semantics -mindepth 1 -printf '%P|%y|%l\n' | sort) \
  <(find -P /candidate/reference-semantics -mindepth 1 -printf '%P|%y|%l\n' | sort)
types_status=$?
echo "SEMANTICS_TYPES_DIFF_EXIT $types_status"
(( types_status == 0 )) || status=1

echo 'COMMAND: recursively compare every supplied-semantics file byte-for-byte'
diff -ruN --no-dereference /reference/reference-semantics /candidate/reference-semantics
semantics_status=$?
echo "SEMANTICS_CONTENT_DIFF_EXIT $semantics_status"
(( semantics_status == 0 )) || status=1

echo 'COMMAND: compute a deterministic reviewer tree digest for each semantics tree'
(
  cd /reference/reference-semantics
  find -P . -type f -print0 | sort -z | xargs -0 sha256sum
) | sha256sum
(
  cd /candidate/reference-semantics
  find -P . -type f -print0 | sort -z | xargs -0 sha256sum
) | sha256sum

echo "FINAL_EXIT $status"
exit "$status"
