#!/usr/bin/env bash
set -eu

audit_stage1_tmp="$(
  sed -n 's/^AUDIT_STAGE1_TMP=//p' /audit-output/evidence/03_semantic.log \
    | tail -n 1
)"
if [ -z "${audit_stage1_tmp}" ] \
  || [ ! -d "${audit_stage1_tmp}/verification-kompiled" ]; then
  printf '%s\n' 'ERROR: independent compiled Stage 1 definition is unavailable'
  exit 1
fi

printf 'AUDIT_STAGE1_TMP=%s\n' "${audit_stage1_tmp}"
cp /audit-output/evidence/spec-vacuity.k "${audit_stage1_tmp}/spec-vacuity.k"
printf '%s\n' '$ kprove deliberately false +1 postcondition mutation (expected failure)'
set +e
(
  cd "${audit_stage1_tmp}"
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module MODP-SPEC-VACUITY \
    -w none
)
mutation_status=$?
set -e
printf 'vacuity_mutation_exit=%s\n' "${mutation_status}"
if [ "${mutation_status}" -eq 0 ]; then
  printf '%s\n' 'ERROR: false postcondition mutation unexpectedly proved'
  exit 1
fi
