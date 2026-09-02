#!/usr/bin/env bash
set -euo pipefail

# Reproduce the translated program.
python3 py2mpy.py solution.py > solution.mpy
python3 check_artifact_identity.py

# Gate C implementation evidence under CPython.
python3 test_solution.py

# Concrete execution uses the required LLVM main module, including the
# reference definition's concrete-only rules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# The proof definition deliberately imports MPY, not MPY-KRUN, and contains no
# task-local semantic rules.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# This is the sole positive target-proof command. It proves every claim in
# SPEC; success requires output #Top and exit status 0.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Negative validation probes: each must be rejected with a genuine stuck claim
# containing its intended symbolic residual.
expect_stuck_claim() {
  local label=$1
  local log_file=$2
  local residual=$3
  shift 3

  local probe_status
  if "$@" >"$log_file" 2>&1
  then
    probe_status=0
  else
    probe_status=$?
  fi

  cat "$log_file"
  if [[ $probe_status -eq 0 ]]
  then
    echo "ERROR: $label unexpectedly proved" >&2
    exit 1
  fi
  rg -Fq "WarnStuckClaimState" "$log_file"
  rg -Fq "$residual" "$log_file"
  echo "EXPECTED FAILURE: $label was rejected with exit $probe_status"
}

expect_stuck_claim \
  "false postcondition mutation" \
  vacuity-probe.log \
  "X +Int Y +Int 1" \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY

expect_stuck_claim \
  "changed-body mutation" \
  body-mutation-probe.log \
  "X -Int Y" \
  kprove spec-body-mutation.k \
    --definition verification-kompiled \
    --spec-module SPEC-BODY-MUTATION
