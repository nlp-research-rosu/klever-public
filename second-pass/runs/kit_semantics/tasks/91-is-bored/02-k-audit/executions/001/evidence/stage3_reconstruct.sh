#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/case91
evidence=/audit-output/evidence
overall=0

run_logged() {
  local label=$1
  shift
  local logfile="$evidence/$label.log"
  (
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    printf 'WORKDIR: %s\n' "$scratch"
    (
      cd "$scratch"
      "$@"
    )
    ec=$?
    printf 'EXIT_STATUS=%d\n' "$ec"
    exit "$ec"
  ) > "$logfile" 2>&1
  local ec=$?
  printf '%s=%d\n' "$label" "$ec"
  if [[ $ec -ne 0 ]]; then overall=1; fi
}

(
  printf 'COMMAND: cd %s && python3 py2mpy.py audit-concrete.py > audit-concrete.mpy\n' "$scratch"
  (
    cd "$scratch"
    python3 py2mpy.py audit-concrete.py > audit-concrete.mpy
  )
  ec=$?
  printf 'EXIT_STATUS=%d\n' "$ec"
  exit "$ec"
) > "$evidence/stage3_translate_concrete.log" 2>&1
ec=$?
printf 'stage3_translate_concrete=%d\n' "$ec"
if [[ $ec -ne 0 ]]; then overall=1; fi

run_logged stage3_kompile_llvm \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

run_logged stage3_krun_concrete \
  krun audit-concrete.mpy \
  --definition audit-runtime-kompiled

run_logged stage3_kompile_connection \
  kompile --backend haskell connection.k \
  --main-module CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-connection-kompiled

run_logged stage3_kprove_connection \
  kprove connection-spec.k \
  --definition audit-connection-kompiled \
  --spec-module CONNECTION-SPEC

run_logged stage3_kompile_base \
  kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-base-kompiled

run_logged stage3_kprove_loop \
  kprove loop-spec.k \
  --definition audit-verification-base-kompiled \
  --spec-module LOOP-SPEC

run_logged stage3_kompile_verification \
  kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

run_logged stage3_kprove_target \
  kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC

printf 'FINAL_STATUS=%d\n' "$overall"
exit "$overall"
