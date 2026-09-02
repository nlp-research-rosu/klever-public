#!/usr/bin/env bash
set -u

work="/tmp/audit-work/reconstruction"
log_dir="/audit-output/evidence/adequacy"
mkdir -p "${log_dir}"
summary="${log_dir}/summary.log"
: >"${summary}"

run_proof() {
  expected=$1
  name=$2
  shift 2
  out="${log_dir}/${name}.log"
  printf 'COMMAND:' >"${out}"
  printf ' %q' "$@" >>"${out}"
  printf '\n' >>"${out}"
  "$@" >>"${out}" 2>&1
  status=$?
  if grep -qx '#Top' "${out}"; then top=yes; else top=no; fi
  printf 'PRINTED_EXACT_TOP_LINE: %s\n' "${top}" >>"${out}"
  printf 'EXIT_STATUS: %s\n' "${status}" >>"${out}"
  printf '%s EXPECTED=%s EXIT_STATUS=%s TOP=%s LOG=%s\n' \
    "${name}" "${expected}" "${status}" "${top}" "${out}" >>"${summary}"
  if [[ "${expected}" == success ]]; then
    (( status == 0 )) && [[ "${top}" == yes ]]
    return
  fi
  (( status != 0 )) && [[ "${top}" == no ]]
}

cd "${work}" || exit 1

run_proof success ground_results \
  kprove /audit-output/evidence/ground-witnesses.k \
  -I "${work}" \
  --definition verification-kompiled \
  --spec-module GROUND-WITNESSES
ground_status=$?

run_proof failure fixed_state_preservation \
  kprove /audit-output/evidence/bridge-state-witness.k \
  -I "${work}" \
  --definition verification-base-kompiled \
  --spec-module BRIDGE-STATE-BASE
base_status=$?

run_proof success extended_state_preservation \
  kprove /audit-output/evidence/bridge-state-witness.k \
  -I "${work}" \
  --definition verification-kompiled \
  --spec-module BRIDGE-STATE-EXTENDED
extended_status=$?

if (( ground_status || base_status || extended_status )); then
  exit 1
fi
