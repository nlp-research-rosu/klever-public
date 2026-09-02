#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/84-solve
evidence=/audit-output/evidence
raw=/tmp/audit-work/84-solve/raw-logs
cd "$work"

# Change the body embedded in solutionModule: digit sum 5 returns "0" instead
# of "101". The spec is redirected to this changed program term.
sed '0,/Return(Str("101"))/s//Return(Str("0"))/' \
  verification.k > verification-body-mutant.k
sed 's/requires "verification.k"/requires "verification-body-mutant.k"/' \
  spec.k > spec-body-mutant.k
cp verification-body-mutant.k "$evidence/verification-body-mutant.k"
cp spec-body-mutant.k "$evidence/spec-body-mutant.k"
diff -u verification.k verification-body-mutant.k \
  > "$evidence/stage4-body-mutation.diff" || true

compile_log="$evidence/stage4-body-mutant-kompile.log"
compile_raw="$raw/stage4-body-mutant-kompile.raw.log"
printf '%s\n' \
  'COMMAND: kompile verification-body-mutant.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-body-mutant-audit-kompiled' \
  > "$compile_log"
set +e
kompile verification-body-mutant.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mutant-audit-kompiled \
  > "$compile_raw" 2>&1
compile_status=$?
set -e
{
  printf 'EXIT_STATUS=%s\n' "$compile_status"
  printf 'OUTPUT_LINES=%s\n' "$(wc -l < "$compile_raw")"
  sed -n '1,120p' "$compile_raw"
} >> "$compile_log"
if [[ $compile_status -ne 0 ]]; then
  exit "$compile_status"
fi

proof_log="$evidence/stage4-body-mutant-proof.log"
proof_raw="$raw/stage4-body-mutant-proof.raw.log"
printf '%s\n' \
  'COMMAND: kprove spec-body-mutant.k --definition verification-body-mutant-audit-kompiled --spec-module SPEC --claims SPEC.solve-sum-00-07' \
  > "$proof_log"
set +e
kprove spec-body-mutant.k \
  --definition verification-body-mutant-audit-kompiled \
  --spec-module SPEC \
  --claims SPEC.solve-sum-00-07 \
  > "$proof_raw" 2>&1
proof_status=$?
set -e
{
  printf 'EXIT_STATUS=%s\n' "$proof_status"
  printf 'OUTPUT_LINES=%s\n' "$(wc -l < "$proof_raw")"
  sed -n '1,160p' "$proof_raw"
  if [[ $(wc -l < "$proof_raw") -gt 320 ]]; then
    printf '[... bounded log: middle omitted ...]\n'
    tail -n 160 "$proof_raw"
  else
    sed -n '161,320p' "$proof_raw"
  fi
} >> "$proof_log"
if [[ $proof_status -eq 0 ]]; then
  printf 'ERROR: body mutation unexpectedly proved\n' >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' "$proof_raw"
printf 'EXPECTED_BODY_SENSITIVITY_FAILURE=%s\n' "$proof_status"
