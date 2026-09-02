#!/usr/bin/env bash
set -u
set -o pipefail

SCRATCH=/tmp/audit-work/103-rounded-avg
SRC=$SCRATCH/candidate-src
EVIDENCE=/audit-output/evidence/logs
overall=0

run_logged() {
  local log=$1
  shift
  printf '$' | tee "$log"
  printf ' %q' "$@" | tee -a "$log"
  printf '\n' | tee -a "$log"
  "$@" 2>&1 | tee -a "$log"
  local rc=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$rc" | tee -a "$log"
  if (( rc != 0 )); then
    overall=1
  fi
  return "$rc"
}

printf 'Fresh build roots:\n'
printf '  source=%s\n' "$SRC"
printf '  concrete=%s\n' "$SCRATCH/semantic-audit-kompiled"
printf '  proof=%s\n' "$SCRATCH/verification-audit-kompiled"

run_logged "$EVIDENCE/04-build-concrete-llvm.log" \
  kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/semantic-audit-kompiled"
concrete_build=$?

run_logged "$EVIDENCE/05-build-proof-haskell.log" \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/verification-audit-kompiled"
proof_build=$?

if (( concrete_build == 0 )); then
  run_logged "$EVIDENCE/06-concrete-semantics-compare.log" \
    python3 /audit-output/evidence/concrete_semantics_compare.py
else
  printf 'Concrete comparison skipped because the fresh concrete build failed.\n'
  overall=1
fi

claims=(
  reversed
  integral-midpoint
  half-even-down
  half-even-up
  example-1-5
  example-7-5
  example-10-20
  example-20-33
  render-3
  render-15
  render-26
)

closed=0
if (( proof_build == 0 )); then
  for claim in "${claims[@]}"; do
    log="$EVIDENCE/07-proof-${claim}.log"
    run_logged "$log" \
      kprove spec.k \
      --definition "$SCRATCH/verification-audit-kompiled" \
      --spec-module SPEC \
      --claims "SPEC.$claim" \
      --output pretty
    rc=$?
    if (( rc == 0 )) && grep -Fxq '#Top' "$log"; then
      printf 'CLAIM %s CLOSED exit=0 top=yes\n' "$claim"
      ((closed += 1))
    else
      printf 'CLAIM %s FAILED exit=%d top=%s\n' \
        "$claim" "$rc" "$([[ -f "$log" ]] && grep -Fxq '#Top' "$log" && printf yes || printf no)"
      overall=1
    fi
  done

  run_logged "$EVIDENCE/08-proof-all-claims.log" \
    kprove spec.k \
    --definition "$SCRATCH/verification-audit-kompiled" \
    --spec-module SPEC \
    --output pretty
  all_rc=$?
  if (( all_rc != 0 )) || ! grep -Fxq '#Top' "$EVIDENCE/08-proof-all-claims.log"; then
    overall=1
  fi
else
  printf 'Individual proofs skipped because the fresh proof build failed.\n'
  overall=1
fi

printf 'positive_claims_total=%d\n' "${#claims[@]}"
printf 'positive_claims_closed=%d\n' "$closed"
printf 'stage3_script_status=%d\n' "$overall"
exit "$overall"
