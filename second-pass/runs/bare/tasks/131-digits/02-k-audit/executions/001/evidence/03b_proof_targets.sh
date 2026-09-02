#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/131-digits
proofdef="$scratch/verification-fresh-kompiled"
failures=0

run_proof() {
  label=$1
  shift
  printf '\nPROOF TARGET: %s\n$' "$label"
  printf ' %q' timeout 300s kprove "$@"
  printf '\n'
  output=$(timeout 300s kprove "$@" 2>&1)
  status=$?
  printf '%s\n[exit %d]\n' "$output" "$status"
  if (( status != 0 )) || ! printf '%s\n' "$output" | grep -qx '#Top'; then
    printf 'proof_check=FAIL target=%s\n' "$label"
    failures=1
  else
    printf 'proof_check=PASS target=%s exit=0 output=#Top\n' "$label"
  fi
}

printf 'AUDIT STAGE 3B: EXACT AND MODULAR POSITIVE PROOF TARGETS\n'

# Exact submitted, unlabeled specification: proves both claims together, just
# as the candidate's single positive proof command intends.
run_proof exact-submitted-spec "$scratch/spec.k" \
  --definition "$proofdef" --spec-module SPEC

# Prove the loop theorem by itself.
run_proof loop-theorem-alone "$scratch/03_spec_labeled.k" \
  --definition "$proofdef" --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.loop-invariant

# Modular entry proof: keep both claims available, but mark only the already
# independently proved loop theorem trusted for this invocation.  Thus the
# only remaining proof obligation is entry-contract.
run_proof entry-contract-given-proved-loop "$scratch/03_spec_labeled.k" \
  --definition "$proofdef" --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.entry-contract,SPEC-LABELED.loop-invariant \
  --trusted SPEC-LABELED.loop-invariant

printf '\nstage3b_failures=%d\n' "$failures"
exit "$failures"
