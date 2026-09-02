#!/usr/bin/env bash
set -u

work="/tmp/audit-work/body-sensitivity"
log_dir="/audit-output/evidence/body-sensitivity"
mkdir -p "${log_dir}"

build_log="${log_dir}/build.log"
printf '%s\n' \
  'COMMAND: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-body-mutated-kompiled' \
  >"${build_log}"
(
  cd "${work}" &&
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module VERIFICATION \
    --output-definition verification-body-mutated-kompiled
) >>"${build_log}" 2>&1
build_status=$?
printf 'EXIT_STATUS: %s\n' "${build_status}" >>"${build_log}"

proof_log="${log_dir}/proof.log"
printf '%s\n' \
  'COMMAND: kprove spec.k --definition verification-body-mutated-kompiled --spec-module SPEC' \
  >"${proof_log}"
(
  cd "${work}" &&
  kprove spec.k \
    --definition verification-body-mutated-kompiled \
    --spec-module SPEC
) >>"${proof_log}" 2>&1
proof_status=$?
if grep -qx '#Top' "${proof_log}"; then top=yes; else top=no; fi
printf 'PRINTED_EXACT_TOP_LINE: %s\n' "${top}" >>"${proof_log}"
printf 'EXIT_STATUS: %s\n' "${proof_status}" >>"${proof_log}"

summary="${log_dir}/summary.log"
printf 'BUILD_EXIT_STATUS: %s\n' "${build_status}" >"${summary}"
printf 'PROOF_EXIT_STATUS: %s\n' "${proof_status}" >>"${summary}"
printf 'PROOF_TOP: %s\n' "${top}" >>"${summary}"
printf 'EXPECTED: build succeeds; proof fails after the executed final return changes true->false\n' \
  >>"${summary}"

if (( build_status == 0 && proof_status != 0 )) && [[ "${top}" == no ]]; then
  exit 0
fi
exit 1
