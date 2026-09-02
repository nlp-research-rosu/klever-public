#!/usr/bin/env bash
set -euo pipefail
set -x

python3 /audit-output/evidence/verify_provenance.py
sha256sum \
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
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py
find /candidate /generation-evidence/codex-trace \
  -printf '%y %s %p -> %l\n' \
  | sort
