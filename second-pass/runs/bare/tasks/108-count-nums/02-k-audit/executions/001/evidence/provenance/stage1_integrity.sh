#!/usr/bin/env bash
set -uo pipefail

required_candidate=(
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

overall=0
printf '%s\n' 'CANDIDATE_REQUIRED_ARTIFACTS'
for item in "${required_candidate[@]}"; do
  target="/candidate/$item"
  if [[ ! -e "$target" && ! -L "$target" ]]; then
    printf 'MISSING %s\n' "$target"
    overall=1
  elif [[ -L "$target" ]]; then
    printf 'SYMLINK %s -> %s\n' "$target" "$(readlink "$target")"
    overall=1
  elif [[ ! -f "$target" ]]; then
    printf 'MISTYPED %s type=%s\n' "$target" "$(stat -c %F "$target")"
    overall=1
  else
    printf 'REGULAR %s bytes=%s sha256=%s\n' \
      "$target" "$(stat -c %s "$target")" "$(sha256sum "$target" | cut -d' ' -f1)"
  fi
done

printf '%s\n' 'TRUSTED_REQUIRED_ARTIFACTS'
for target in /reference/prompt.py /reference/canonical.py /reference/py2mpy.py; do
  if [[ -f "$target" && ! -L "$target" ]]; then
    printf 'REGULAR %s bytes=%s sha256=%s\n' \
      "$target" "$(stat -c %s "$target")" "$(sha256sum "$target" | cut -d' ' -f1)"
  else
    printf 'INVALID_OR_MISSING %s\n' "$target"
    overall=1
  fi
done

printf '%s\n' 'GENERATED_SEMANTICS_MODE_BOUNDARY'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf '%s\n' 'BREACH /reference/reference-semantics exists'
  overall=1
else
  printf '%s\n' 'OK /reference/reference-semantics absent'
fi

cmp -s /candidate/prompt.py /reference/prompt.py
prompt_status=$?
printf 'PROMPT_CMP_EXIT: %d\n' "$prompt_status"
(( prompt_status == 0 )) || overall=1

cmp -s /candidate/py2mpy.py /reference/py2mpy.py
translator_status=$?
printf 'TRANSLATOR_CMP_EXIT: %d\n' "$translator_status"
(( translator_status == 0 )) || overall=1

printf '%s\n' 'ALL_CANDIDATE_SYMLINKS'
find /candidate -type l -printf '%p -> %l\n'
printf '%s\n' 'ALL_REFERENCE_SYMLINKS'
find /reference -type l -printf '%p -> %l\n'

printf 'OVERALL_EXIT: %d\n' "$overall"
exit "$overall"
