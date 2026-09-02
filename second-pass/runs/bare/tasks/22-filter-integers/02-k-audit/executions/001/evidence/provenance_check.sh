#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference

required_candidate_files=(
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

printf '%s\n' 'CANDIDATE REQUIRED FILE TYPES'
integrity_status=0
for relative_path in "${required_candidate_files[@]}"; do
  artifact_path="${candidate_root}/${relative_path}"
  if [[ -L "$artifact_path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$artifact_path" "$(readlink "$artifact_path")"
    integrity_status=1
  elif [[ -f "$artifact_path" ]]; then
    printf 'REGULAR %s\n' "$artifact_path"
  elif [[ -e "$artifact_path" ]]; then
    printf 'MISTYPED %s\n' "$artifact_path"
    integrity_status=1
  else
    printf 'MISSING %s\n' "$artifact_path"
    integrity_status=1
  fi
done

printf '%s\n' 'CANDIDATE ROOT INVENTORY'
find "$candidate_root" -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort

printf '%s\n' 'SYMLINK INVENTORY'
find "$candidate_root" -type l -printf '%p -> %l\n' | sort

printf '%s\n' 'STRUCTURED TRACE FILES'
find "$candidate_root/codex-trace" -type f -printf '%p %s bytes\n' | sort

printf '%s\n' 'GENERATED-SEMANTICS MOUNT CHECK'
if [[ -e "$reference_root/reference-semantics" ||
      -L "$reference_root/reference-semantics" ]]; then
  printf '%s\n' 'BREACH: /reference/reference-semantics exists'
  integrity_status=1
else
  printf '%s\n' 'OK: /reference/reference-semantics is absent'
fi

printf '%s\n' 'TRUSTED FILE COMPARISONS'
for comparison_name in prompt.py py2mpy.py; do
  candidate_path="${candidate_root}/${comparison_name}"
  reference_path="${reference_root}/${comparison_name}"
  sha256sum "$candidate_path" "$reference_path"
  if cmp --silent "$candidate_path" "$reference_path"; then
    printf 'BYTE_IDENTICAL %s\n' "$comparison_name"
  else
    printf 'CHANGED %s\n' "$comparison_name"
    integrity_status=1
  fi
done

exit "$integrity_status"
