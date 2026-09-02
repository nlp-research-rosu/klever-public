#!/usr/bin/env bash
set -u
set -x

find /reference -maxdepth 2 -printf '%y %p -> %l\n' | sort
find /candidate -maxdepth 2 -printf '%y %p -> %l\n' | sort
find /candidate -type l -printf '%p -> %l\n'
test ! -e /reference/reference-semantics
cmp --silent /reference/prompt.py /candidate/prompt.py
prompt_cmp_exit=$?
cmp --silent /reference/py2mpy.py /candidate/py2mpy.py
translator_cmp_exit=$?
sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
wc -c \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-21-56-019f8958-a5ad-71f1-ac10-56738b98ca18.jsonl
printf 'prompt_cmp_exit=%s\n' "$prompt_cmp_exit"
printf 'translator_cmp_exit=%s\n' "$translator_cmp_exit"
printf 'required_generated_sources:\n'
for artifact in solution.py solution.mpy semantic.k verification.k spec.k prove.sh; do
  if test -f "/candidate/$artifact" && ! test -L "/candidate/$artifact"; then
    printf 'regular_file %s\n' "$artifact"
  else
    printf 'MISSING_OR_MISTYPED %s\n' "$artifact"
  fi
done
