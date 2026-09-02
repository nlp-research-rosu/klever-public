#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference

printf '%s\n' 'SEMANTICS BOUNDARY'
if [[ -e "$reference_root/reference-semantics" || -L "$reference_root/reference-semantics" ]]; then
  printf '%s\n' 'BREACH: /reference/reference-semantics exists in GENERATED_SEMANTICS mode'
  boundary_status=1
else
  printf '%s\n' 'OK: /reference/reference-semantics is absent as required'
  boundary_status=0
fi

printf '%s\n' 'TRUSTED INPUT TYPES'
for trusted_path in \
  "$reference_root/canonical.py" \
  "$reference_root/prompt.py" \
  "$reference_root/py2mpy.py"
do
  stat --printf='%F %a %n\n' "$trusted_path"
  if [[ ! -f "$trusted_path" || -L "$trusted_path" ]]; then
    printf 'INTEGRITY FAILURE: non-regular or symlinked trusted input %s\n' "$trusted_path"
  fi
done

printf '%s\n' 'CANDIDATE TREE TYPES'
find "$candidate_root" -mindepth 1 -maxdepth 4 \
  -printf '%y %m %s %p -> %l\n' | LC_ALL=C sort

printf '%s\n' 'REQUIRED CANDIDATE ARTIFACT TYPES'
for candidate_name in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k \
  verification.k spec.k
do
  candidate_path="$candidate_root/$candidate_name"
  if [[ ! -e "$candidate_path" && ! -L "$candidate_path" ]]; then
    printf 'MISSING %s\n' "$candidate_path"
  else
    stat --printf='%F %a %s %n\n' "$candidate_path"
    if [[ ! -f "$candidate_path" || -L "$candidate_path" ]]; then
      printf 'INTEGRITY FAILURE: non-regular or symlinked %s\n' "$candidate_path"
    fi
  fi
done

printf '%s\n' 'PROMPT AND TRANSLATOR BYTE COMPARISONS'
for artifact_name in prompt.py py2mpy.py
do
  sha256sum "$candidate_root/$artifact_name" "$reference_root/$artifact_name"
  if cmp -s "$candidate_root/$artifact_name" "$reference_root/$artifact_name"; then
    printf 'BYTE_IDENTICAL %s\n' "$artifact_name"
  else
    printf 'BYTE_DIFFERENT %s\n' "$artifact_name"
  fi
done

printf '%s\n' 'CANDIDATE K SOURCE FILES'
find "$candidate_root" -path "$candidate_root/verification-kompiled" -prune -o \
  -type f -name '*.k' -printf '%p\n' | LC_ALL=C sort

printf '%s\n' 'CANDIDATE TOP-LEVEL SYMLINKS'
find "$candidate_root" -mindepth 1 -maxdepth 1 -type l \
  -printf '%p -> %l\n' | LC_ALL=C sort

printf '%s\n' 'UNTRUSTED CLAIM FILE HASHES'
sha256sum \
  "$candidate_root/run-input.json" \
  "$candidate_root/metrics.json" \
  "$candidate_root/codex-last.txt" \
  "$candidate_root/codex-output.log"

exit "$boundary_status"
