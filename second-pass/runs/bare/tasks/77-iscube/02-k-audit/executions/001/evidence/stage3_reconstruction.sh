#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/77-iscube
src="$scratch/candidate-src"
semdef="$scratch/audit-semantic-kompiled"
cubedef="$scratch/audit-cube-verification-kompiled"
gapdef="$scratch/audit-gap-verification-kompiled"

printf 'Fresh-output prechecks (all must be absent):\n'
run test '!' -e "$semdef"
run test '!' -e "$cubedef"
run test '!' -e "$gapdef"

run kompile "$src/semantic.k" \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition "$semdef"
semantic_build_status=$?

if (( semantic_build_status == 0 )); then
  printf '\nConcrete generated-semantics/Python comparisons:\n'
  inputs=(-65 -64 -63 -2 -1 0 1 2 7 8 9 26 27 28 64 180)
  for input in "${inputs[@]}"; do
    printf '\n$ krun %q -cN=%q --definition %q\n' \
      "$src/solution.mpy" "$input" "$semdef"
    krun_output="$(krun "$src/solution.mpy" -cN="$input" --definition "$semdef" 2>&1)"
    krun_status=$?
    printf '%s\n' "$krun_output"
    printf '[exit %d]\n' "$krun_status"

    printf '$ python3 -c <import copied solution; call iscube(%q)>\n' "$input"
    python_output="$(
      INPUT_VALUE="$input" SOLUTION_PATH="$src/solution.py" python3 - <<'PY'
import importlib.util
import os
spec = importlib.util.spec_from_file_location("generated", os.environ["SOLUTION_PATH"])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(str(module.iscube(int(os.environ["INPUT_VALUE"]))).lower())
PY
    )"
    python_status=$?
    printf '%s\n' "$python_output"
    printf '[exit %d]\n' "$python_status"

    if (( krun_status != 0 || python_status != 0 )); then
      printf 'COMPARE input=%s status=ERROR\n' "$input"
    elif grep -Eq "BoolVal[[:space:]]*\\([[:space:]]*$python_output[[:space:]]*\\)" \
      <<<"$krun_output"; then
      printf 'COMPARE input=%s expected=%s status=MATCH\n' "$input" "$python_output"
    else
      printf 'COMPARE input=%s expected=%s status=MISMATCH\n' "$input" "$python_output"
    fi
  done
fi

run kompile "$src/verification.k" \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  --output-definition "$cubedef"
cube_build_status=$?

if (( cube_build_status == 0 )); then
  run kprove "$src/spec.k" \
    --definition "$cubedef" \
    --spec-module CUBE-SPEC

  for label in cube-loop nonnegative-cube negative-cube; do
    run kprove "$src/spec.k" \
      --definition "$cubedef" \
      --spec-module CUBE-SPEC \
      --claims "CUBE-SPEC.$label"
  done
fi

run kompile "$src/verification.k" \
  --main-module GAP-VERIFICATION \
  --syntax-module GAP-VERIFICATION \
  --backend haskell \
  --output-definition "$gapdef"
gap_build_status=$?

if (( gap_build_status == 0 )); then
  run kprove "$src/spec.k" \
    --definition "$gapdef" \
    --spec-module GAP-SPEC

  for label in gap-loop positive-noncube negative-noncube; do
    run kprove "$src/spec.k" \
      --definition "$gapdef" \
      --spec-module GAP-SPEC \
      --claims "GAP-SPEC.$label"
  done
fi
