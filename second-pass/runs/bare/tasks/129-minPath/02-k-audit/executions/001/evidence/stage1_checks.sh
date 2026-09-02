#!/usr/bin/env bash
set +e

printf '%s\n' '=== REQUIRED TYPES ==='
for candidate_path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh
do
  if [ -e "$candidate_path" ] || [ -L "$candidate_path" ]; then
    stat -c '%F|%a|%s|%n|%N' "$candidate_path"
  else
    printf 'MISSING|%s\n' "$candidate_path"
  fi
done

printf '%s\n' '=== TRACE TYPES ==='
find /candidate/codex-trace \( -type l -o -type f \) \
  -printf '%y|%s|%p|%l\n' | sort

printf '%s\n' '=== TRUSTED IDENTITY ==='
sha256sum \
  /candidate/prompt.py \
  /reference/prompt.py \
  /candidate/py2mpy.py \
  /reference/py2mpy.py
cmp -s /candidate/prompt.py /reference/prompt.py
printf 'PROMPT_CMP=%s\n' "$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'TRANSLATOR_CMP=%s\n' "$?"

printf '%s\n' '=== GENERATED MODE MOUNT ==='
if [ -e /reference/reference-semantics ] || [ -L /reference/reference-semantics ]; then
  printf '%s\n' 'reference-semantics PRESENT'
else
  printf '%s\n' 'reference-semantics ABSENT'
fi
