#!/usr/bin/env bash
set -uo pipefail

status=0

echo "Required mount types"
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
  if [[ -r "$path" ]]; then
    printf 'READABLE %s type=%s\n' "$path" "$(stat -c %F "$path")"
  else
    printf 'MISSING_OR_UNREADABLE %s\n' "$path"
    status=1
  fi
done

echo "Required file SHA-256 values"
sha256sum \
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
  /generation-evidence/legacy-metrics.json \
  /generation-evidence/legacy-run-input.json \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T21-18-11-019f8cc4-2204-79c0-90c8-74fabe114144.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

echo "Campaign-lock structured equality"
python3 -c 'import json; a=json.load(open("/audit-input.json")); b=json.load(open("/audit-campaign-lock.json")); print(a["audit_campaign"] == b); raise SystemExit(a["audit_campaign"] != b)'
(( status |= $? ))

echo "Candidate prompt byte comparison"
cmp /candidate/prompt.py /reference/prompt.py
(( status |= $? ))

echo "Candidate translator byte comparison"
cmp /candidate/py2mpy.py /reference/py2mpy.py
(( status |= $? ))

echo "Supplied-semantics recursive entry and byte comparison"
diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
(( status |= $? ))

echo "Symlink scan (expected: no output)"
find /candidate /reference /generation-evidence -type l -print
if find /candidate/reference-semantics -type l -print -quit | grep -q .; then
  status=1
fi

echo "Supplied-semantics per-file hashes"
(
  cd /candidate/reference-semantics || exit 1
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)
(( status |= $? ))
(
  cd /reference/reference-semantics || exit 1
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)
(( status |= $? ))

echo "Candidate entry inventory and per-file hashes"
find /candidate -printf '%y %p -> %l\n' | sort
(
  cd /candidate || exit 1
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)
(( status |= $? ))

exit "$status"
