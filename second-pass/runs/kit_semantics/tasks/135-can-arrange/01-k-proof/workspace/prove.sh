#!/usr/bin/env bash
set -euo pipefail

mkdir -p evidence

python3 py2mpy.py solution.py > solution.mpy
python3 check_program_identity.py | tee evidence/program-identity.log
sha256sum solution.py solution.mpy | tee evidence/program-hashes.log
python3 -m py_compile solution.py differential_test.py

python3 py2mpy.py smoke.py > smoke.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  2>&1 | tee evidence/llvm-kompile.log
krun smoke.mpy --definition runtime-kompiled \
  2>&1 | tee evidence/krun-smoke.log

python3 differential_test.py | tee evidence/differential.log

# Bridge-free connection definition and its ten complete static cases.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled \
  2>&1 | tee evidence/connection-kompile.log
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC \
  2>&1 | tee evidence/connection-kprove.log

# Positive target proof: both the loop circularity and whole-program claim.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  2>&1 | tee evidence/verification-kompile.log
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee evidence/target-kprove.log

run_expected_failure() {
  local log_file=$1
  shift
  set +e
  "$@" >"$log_file" 2>&1
  local status=$?
  set -e
  cat "$log_file"
  if [[ $status -eq 0 ]]; then
    echo "UNEXPECTED SUCCESS: $*" >&2
    return 1
  fi
  grep -q "WarnStuckClaimState" "$log_file"
  echo "EXPECTED FAILURE (exit $status): $*"
}

run_expected_failure evidence/spec-vacuity.log \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY

run_expected_failure evidence/body-mutation.log \
  kprove body-mutation-spec.k \
    --definition verification-kompiled \
    --spec-module BODY-MUTATION-SPEC

run_expected_failure evidence/connection-negative.log \
  kprove connection-negative-spec.k \
    --definition connection-kompiled \
    --spec-module CONNECTION-NEGATIVE-SPEC
