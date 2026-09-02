#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/proof-audit || exit 97

printf '[satisfying concrete Python witnesses]\n'
run python3 /audit-output/evidence/ground_witness.py

printf '[copy reviewer claims into scratch and verify their identity]\n'
run cp /audit-output/evidence/spec-ground.k ./spec-ground.k
run cp /audit-output/evidence/spec-vacuity.k ./spec-vacuity.k
run cmp -s /audit-output/evidence/spec-ground.k ./spec-ground.k
run cmp -s /audit-output/evidence/spec-vacuity.k ./spec-vacuity.k
run sha256sum ./spec-ground.k ./spec-vacuity.k

printf '[three ground substitutions against fixed semantics]\n'
run kprove spec-ground.k \
  --definition verification-kompiled \
  --spec-module SPEC-GROUND

printf '[fresh false result mutation: expected meaningful proof failure]\n'
run kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
