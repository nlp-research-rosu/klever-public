#!/usr/bin/env bash
set -u

status=0

echo '$ sha256sum launcher-declared mounted files'
sha256sum \
  /audit-campaign-lock.json \
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
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T02-15-07-019f9820-b0e7-7a62-afb4-ee4e0c84353c.jsonl \
  || status=1

echo '$ compare audit_campaign block with campaign lock'
node -e '
const fs = require("fs");
const input = JSON.parse(fs.readFileSync("/audit-input.json", "utf8"));
const lock = JSON.parse(fs.readFileSync("/audit-campaign-lock.json", "utf8"));
if (JSON.stringify(input.audit_campaign) !== JSON.stringify(lock)) {
  console.log("MISMATCH");
  process.exit(1);
}
console.log("MATCH");
' || status=1

echo '$ find symlinks in protected mounted trees'
symlinks="$(
  find /candidate /reference /generation-evidence -type l \
    -printf '%p -> %l\n'
)"
if test -n "$symlinks"; then
  printf '%s\n' "$symlinks"
  status=1
else
  echo 'none'
fi

echo '$ cmp candidate prompt against trusted prompt'
cmp /candidate/prompt.py /reference/prompt.py || status=1

echo '$ cmp candidate translator against trusted translator'
cmp /candidate/py2mpy.py /reference/py2mpy.py || status=1

echo '$ diff candidate supplied semantics against trusted supplied semantics'
diff -qr --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics \
  || status=1

echo "EXIT_STATUS=$status"
exit "$status"
