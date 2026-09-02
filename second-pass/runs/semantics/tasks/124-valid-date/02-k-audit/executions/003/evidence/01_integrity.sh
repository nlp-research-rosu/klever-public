#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/01_integrity.log

{
  printf '%s\n' 'COMMAND: python3 /audit-output/evidence/01_integrity.py'
  python3 /audit-output/evidence/01_integrity.py
  STATUS=$?
  printf 'EXIT_STATUS: %s\n' "$STATUS"

  printf '%s\n' 'COMMAND: sha256sum launcher-declared regular inputs'
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
    /generation-evidence/codex-trace/2026/07/23/*.jsonl \
    /candidate/prompt.py \
    /candidate/py2mpy.py \
    /reference/prompt.py \
    /reference/py2mpy.py \
    /reference/canonical.py
  printf 'EXIT_STATUS: %s\n' "$?"

  printf '%s\n' 'COMMAND: diff -qr --no-dereference candidate/trusted semantics'
  diff -qr --no-dereference \
    /candidate/reference-semantics \
    /reference/reference-semantics
  printf 'EXIT_STATUS: %s\n' "$?"
} >"$LOG" 2>&1

sed -n '1,280p' "$LOG"
