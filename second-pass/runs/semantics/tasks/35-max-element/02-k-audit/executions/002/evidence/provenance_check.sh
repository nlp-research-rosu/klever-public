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

printf 'Stage 1 independent provenance and integrity checks\n'
run sha256sum \
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
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T23-03-06-019f8d24-2cbe-7ac0-a0ea-9ae7e6694037.jsonl

run python3 -c 'import json; a=json.load(open("/audit-input.json")); c=json.load(open("/audit-campaign-lock.json")); assert a["audit_campaign"] == c; print("campaign block equals lock JSON")'
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics

printf '\nCandidate reference-semantics entry types:\n'
run find /candidate/reference-semantics -printf '%y %P -> %l\n'
printf '\nTrusted reference-semantics entry types:\n'
run find /reference/reference-semantics -printf '%y %P -> %l\n'

printf '\nSymlinks in launcher-controlled and candidate trees (expected: none):\n'
run find \
  /candidate \
  /reference \
  /generation-evidence \
  -type l -printf '%p -> %l\n'

printf '\nRequired legacy-selected-stage1 records and candidate deliverables:\n'
required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
)
for path in "${required[@]}"; do
  if test -r "$path"; then
    stat -c 'OK type=%F mode=%a path=%n' "$path"
  else
    printf 'MISSING_OR_UNREADABLE %s\n' "$path"
  fi
done

printf '\nReviewer content-manifest hashes (path plus file content hash):\n'
for tree in /candidate /reference/reference-semantics /generation-evidence/codex-trace; do
  printf 'TREE %s\n' "$tree"
  while IFS= read -r -d '' rel; do
    hash=$(sha256sum "$tree/$rel" | cut -d' ' -f1)
    printf '%s  %s\n' "$hash" "$rel"
  done < <(find "$tree" -type f -printf '%P\0' | sort -z)
done
