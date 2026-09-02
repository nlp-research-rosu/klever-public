#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/candidate
build_root=/tmp/audit-work/bridge-build-2
proof_definition=/tmp/audit-work/fresh-build/verification-kompiled
llvm_definition=/tmp/audit-work/fresh-build/runtime-kompiled

mkdir -p "$build_root"

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@"
  status=$?
  set -e
  printf 'EXIT_STATUS=%s\n' "$status"
  return "$status"
}

negative_index=0
run_expected_nonzero() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  negative_index=$((negative_index + 1))
  raw="$build_root/expected-nonzero-$negative_index.raw.log"
  set +e
  "$@" >"$raw" 2>&1
  status=$?
  set -e
  sed -n '1,50p' "$raw"
  rg -n -m 80 'sortEquality|WarnStuckClaimState|implication check|#Equals|\\[Error\\]|<exc>|<exit-code>' "$raw" || true
  tail -20 "$raw"
  printf 'EXIT_STATUS=%s\n' "$status"
  if [ "$status" -eq 0 ]; then
    printf 'EXPECTED_NONZERO_BUT_SUCCEEDED\n'
    return 1
  fi
  return 0
}

cp /audit-output/evidence/connection-verification.k "$scratch/connection-verification.k"
cp /audit-output/evidence/connection-spec.k "$scratch/connection-spec.k"

run bash -c 'python3 "$1" "$2" > "$3"' _ \
  /reference/py2mpy.py /audit-output/evidence/list_equality_probe.py \
  "$build_root/list-equality-probe.mpy"
run bash -c 'python3 "$1" "$2" > "$3"' _ \
  /reference/py2mpy.py /audit-output/evidence/sort_bridge_probe.py \
  "$build_root/sort-bridge-probe.mpy"

run kompile "$scratch/reference-semantics/semantics.k" \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/fixed-haskell-kompiled"

run krun "$build_root/list-equality-probe.mpy" \
  --definition "$build_root/fixed-haskell-kompiled"
run_expected_nonzero krun "$build_root/list-equality-probe.mpy" \
  --definition "$proof_definition"

run krun "$build_root/sort-bridge-probe.mpy" \
  --definition "$llvm_definition"
run_expected_nonzero krun "$build_root/sort-bridge-probe.mpy" \
  --definition "$proof_definition"

run kompile "$scratch/connection-verification.k" \
  --backend haskell \
  --main-module CONNECTION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/connection-kompiled"

run_expected_nonzero kprove "$scratch/connection-spec.k" \
  --definition "$build_root/connection-kompiled" \
  --spec-module CONNECTION-SPEC

printf 'BRIDGE_AUDIT_RUN=PASS\n'
