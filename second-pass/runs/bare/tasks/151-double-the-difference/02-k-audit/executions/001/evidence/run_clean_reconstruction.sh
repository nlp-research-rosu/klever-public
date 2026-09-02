#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/candidate-src
BUILD=/tmp/audit-work/build-verified

record_status() {
  local label="$1"
  local status="$2"
  printf '%s_EXIT_STATUS=%s\n' "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    exit "$status"
  fi
}

mkdir -p "$BUILD"
cp /audit-output/evidence/spec-labeled.k "$WORK/spec-labeled.k"

printf '%s\n' 'COMMAND: kompile --version'
kompile --version
status=$?
record_status KOMPILE_VERSION "$status"

printf '%s\n' 'COMMAND: kprove --version'
kprove --version
status=$?
record_status KPROVE_VERSION "$status"

printf '%s\n' \
  'COMMAND: kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/build-verified/semantic-kompiled'
timeout 300 kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/semantic-kompiled"
status=$?
record_status FRESH_SEMANTICS_KOMPILE "$status"

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/semantics_dynamic_test.py'
python3 /audit-output/evidence/semantics_dynamic_test.py
status=$?
record_status SEMANTICS_DYNAMIC "$status"

printf '%s\n' \
  'COMMAND: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/build-verified/verification-kompiled'
timeout 300 kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD/verification-kompiled"
status=$?
record_status FRESH_VERIFICATION_KOMPILE "$status"

printf '%s\n' \
  'COMMAND: kprove spec.k --definition /tmp/audit-work/build-verified/verification-kompiled --spec-module SPEC'
timeout 300 kprove spec.k \
  --definition "$BUILD/verification-kompiled" \
  --spec-module SPEC
status=$?
record_status ORIGINAL_SPEC_ALL_CLAIMS "$status"

printf '%s\n' \
  'COMMAND: kprove spec-labeled.k --definition /tmp/audit-work/build-verified/verification-kompiled --spec-module SPEC-AUDIT --claims SPEC-AUDIT.loop-audit'
timeout 300 kprove spec-labeled.k \
  --definition "$BUILD/verification-kompiled" \
  --spec-module SPEC-AUDIT \
  --claims SPEC-AUDIT.loop-audit
status=$?
record_status LABELED_LOOP_CLAIM "$status"
