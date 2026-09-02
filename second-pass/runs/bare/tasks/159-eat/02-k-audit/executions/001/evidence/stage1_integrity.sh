#!/usr/bin/env bash
set -u

required=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
  prove.sh
)

printf 'SEMANTICS_MODE=GENERATED_SEMANTICS\n'
if [[ -e /reference/reference-semantics ]]; then
  printf 'BOUNDARY=BREACH: /reference/reference-semantics exists\n'
else
  printf 'BOUNDARY=OK: /reference/reference-semantics absent\n'
fi

for name in "${required[@]}"; do
  path=/candidate/$name
  if [[ -L "$path" ]]; then
    printf 'REQUIRED %s: SYMLINK -> %s\n' "$name" "$(readlink "$path")"
  elif [[ -f "$path" ]]; then
    printf 'REQUIRED %s: regular file\n' "$name"
  elif [[ -e "$path" ]]; then
    printf 'REQUIRED %s: WRONG TYPE\n' "$name"
  else
    printf 'REQUIRED %s: MISSING\n' "$name"
  fi
done

if cmp -s /candidate/prompt.py /reference/prompt.py; then
  printf 'PROMPT_IDENTITY=BYTE_IDENTICAL\n'
else
  printf 'PROMPT_IDENTITY=DIFFERENT\n'
fi

if cmp -s /candidate/py2mpy.py /reference/py2mpy.py; then
  printf 'TRANSLATOR_IDENTITY=BYTE_IDENTICAL\n'
else
  printf 'TRANSLATOR_IDENTITY=DIFFERENT\n'
fi

printf 'SOURCE_HASHES\n'
sha256sum \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/canonical.py

printf 'CANDIDATE_SYMLINKS\n'
find /candidate -type l -printf '%p -> %l\n'

printf 'CANDIDATE_TOP_LEVEL_ENTRIES\n'
find /candidate -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort
