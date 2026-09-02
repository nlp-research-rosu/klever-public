#!/usr/bin/env bash
set -u

run_logged() {
  local label="$1"
  shift
  local log="/audit-output/evidence/${label}.log"
  {
    printf 'CWD: %s\n' "$PWD"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf 'EXIT_STATUS: %d\n' "$status"
    return "$status"
  } >"$log" 2>&1
}

cd /tmp/audit-work/68-pluck || exit 90

run_logged 09-pinning-extract \
  python3 /audit-output/evidence/pinning_extract.py
extract_status=$?

run_logged 10-kast-solution \
  kast --definition audit-verification-kompiled \
    --input program --output kore \
    --output-file solution-parsed.kore solution.mpy
solution_kast_status=$?

run_logged 11-kast-claim-program \
  kast --definition audit-verification-kompiled \
    --input program --output kore \
    --output-file claim-program-parsed.kore claim-extracted-program.mpy
claim_kast_status=$?

run_logged 12-constructor-compare bash -c \
  'cmp -s solution-parsed.kore claim-program-parsed.kore && sha256sum solution-parsed.kore claim-program-parsed.kore'
constructor_status=$?

run_logged 13-ground-summary-proof \
  kprove spec-ground-summaries.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-GROUND-SUMMARIES
summary_status=$?

run_logged 14-translate-runtime-witness bash -c \
  'python3 py2mpy.py audit-witness.py > audit-witness.mpy && sha256sum audit-witness.py audit-witness.mpy'
witness_translation_status=$?

if [[ -e audit-runtime-kompiled ]]; then
  printf 'Refusing to reuse pre-existing audit-runtime-kompiled\n' >&2
  exit 91
fi

run_logged 15-kompile-runtime \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled
runtime_build_status=$?

if (( runtime_build_status == 0 )); then
  run_logged 16-krun-runtime-witness \
    krun audit-witness.mpy --definition audit-runtime-kompiled
  runtime_witness_status=$?
else
  runtime_witness_status=99
fi

if [[ -e audit-projection-kompiled ]]; then
  printf 'Refusing to reuse pre-existing audit-projection-kompiled\n' >&2
  exit 92
fi

run_logged 17-kompile-projection-base \
  kompile verification-projection-base.k \
    --backend haskell \
    --main-module PROJECTION-BASE \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-projection-kompiled
projection_build_status=$?

if (( projection_build_status == 0 )); then
  run_logged 18-projection-connection-proof \
    kprove spec-projection-connection.k \
      --definition audit-projection-kompiled \
      --spec-module SPEC-PROJECTION-CONNECTION
  projection_proof_status=$?
else
  projection_proof_status=99
fi

printf '%s\n' \
  "extract=$extract_status solution_kast=$solution_kast_status claim_kast=$claim_kast_status" \
  "constructor=$constructor_status summary=$summary_status witness_translate=$witness_translation_status" \
  "runtime_build=$runtime_build_status runtime_witness=$runtime_witness_status" \
  "projection_build=$projection_build_status projection_proof=$projection_proof_status"

if (( extract_status != 0 || solution_kast_status != 0 ||
      claim_kast_status != 0 || constructor_status != 0 ||
      summary_status != 0 || witness_translation_status != 0 ||
      runtime_build_status != 0 || runtime_witness_status != 0 ||
      projection_build_status != 0 || projection_proof_status != 0 )); then
  exit 1
fi
