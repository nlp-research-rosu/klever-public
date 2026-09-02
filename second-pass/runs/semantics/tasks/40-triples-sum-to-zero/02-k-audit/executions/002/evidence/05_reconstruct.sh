#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
overall=0

run_logged() {
  local log=$1
  shift
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    status=$?
    printf 'EXIT_STATUS=%s\n' "$status"
  } > "$log" 2>&1
  printf '%s exit=%s\n' "$(basename "$log")" "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

cd "$work"
test ! -e runtime-kompiled
test ! -e verification-kompiled

run_logged "$evidence/05_versions.log" bash -c \
  'kompile --version && krun --version && kprove --version'

run_logged "$evidence/05_concrete_regeneration.log" bash -c \
  'python3 py2mpy.py concrete_tests.py > concrete_tests.regenerated.mpy && cmp concrete_tests.regenerated.mpy concrete_tests.mpy && sha256sum concrete_tests.regenerated.mpy concrete_tests.mpy'

run_logged "$evidence/05_kompile_llvm.log" \
  timeout 900 kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-kompiled

run_logged "$evidence/05_krun_concrete.log" \
  timeout 300 krun concrete_tests.regenerated.mpy \
    --definition runtime-kompiled

run_logged "$evidence/05_kompile_haskell.log" \
  timeout 900 kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-kompiled

run_logged "$evidence/05_kprove_batch.log" \
  timeout 900 kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC \
    --output pretty

for label in empty length-one length-two length-three length-four length-five length-six; do
  run_logged "$evidence/05_kprove_${label}.log" \
    timeout 900 kprove spec.k \
      --definition verification-kompiled \
      --spec-module SPEC \
      --claims "SPEC.${label}" \
      --output pretty
done

exit "$overall"
