#!/usr/bin/env bash
set -o pipefail

echo 'COMMAND: test ! -e /reference/reference-semantics'
test ! -e /reference/reference-semantics
rc=$?
echo "EXIT: $rc"

echo 'COMMAND: find /candidate -type l -print'
find /candidate -type l -print
rc=$?
echo "EXIT: $rc"

echo 'COMMAND: cmp candidate prompt and translator against trusted references'
cmp -s /candidate/prompt.py /reference/prompt.py
prompt_rc=$?
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
translator_rc=$?
echo "prompt_cmp_exit=$prompt_rc translator_cmp_exit=$translator_rc"

echo 'COMMAND: sha256sum key inputs'
sha256sum \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/spec.k \
  /candidate/verification.k \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py
rc=$?
echo "EXIT: $rc"

if (( prompt_rc != 0 || translator_rc != 0 )); then
  exit 1
fi
