#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 90
definition=verification-haskell-kompiled

run_claim() {
  label=$1
  spec_file=$2
  spec_module=$3
  printf 'COMMAND[%s]: kprove %s --definition %s --spec-module %s\n' \
    "$label" "$spec_file" "$definition" "$spec_module"
  kprove "$spec_file" --definition "$definition" --spec-module "$spec_module"
  status=$?
  printf 'EXIT[%s]=%s\n' "$label" "$status"
  if test "$status" -ne 0; then
    return "$status"
  fi
}

run_claim original-all spec.k MODP-SPEC || exit $?
run_claim general audit-specs.k AUDIT-SPEC-GENERAL || exit $?
run_claim example-3-5 audit-specs.k AUDIT-SPEC-EXAMPLE-3-5 || exit $?
run_claim example-1101-101 audit-specs.k AUDIT-SPEC-EXAMPLE-1101-101 || exit $?
run_claim example-0-101 audit-specs.k AUDIT-SPEC-EXAMPLE-0-101 || exit $?
run_claim example-3-11 audit-specs.k AUDIT-SPEC-EXAMPLE-3-11 || exit $?
run_claim example-100-101 audit-specs.k AUDIT-SPEC-EXAMPLE-100-101 || exit $?
