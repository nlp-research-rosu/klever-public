#!/usr/bin/env bash
set -u

work="/tmp/audit-work/reconstruction"
log_dir="/audit-output/evidence/reconstruction"
mkdir -p "${log_dir}"
summary="${log_dir}/summary.log"
: >"${summary}"
failed=0

run_logged() {
  name=$1
  shift
  out="${log_dir}/${name}.log"
  printf 'COMMAND:' >"${out}"
  printf ' %q' "$@" >>"${out}"
  printf '\n' >>"${out}"
  "$@" >>"${out}" 2>&1
  status=$?
  printf 'EXIT_STATUS: %s\n' "${status}" >>"${out}"
  printf '%s EXIT_STATUS=%s LOG=%s\n' "${name}" "${status}" "${out}" \
    >>"${summary}"
  if (( status != 0 )); then
    failed=1
  fi
  return 0
}

run_proof() {
  name=$1
  shift
  out="${log_dir}/${name}.log"
  printf 'COMMAND:' >"${out}"
  printf ' %q' "$@" >>"${out}"
  printf '\n' >>"${out}"
  "$@" >>"${out}" 2>&1
  status=$?
  if grep -qx '#Top' "${out}"; then
    top=yes
  else
    top=no
  fi
  printf 'PRINTED_EXACT_TOP_LINE: %s\n' "${top}" >>"${out}"
  printf 'EXIT_STATUS: %s\n' "${status}" >>"${out}"
  printf '%s EXIT_STATUS=%s TOP=%s LOG=%s\n' \
    "${name}" "${status}" "${top}" "${out}" >>"${summary}"
  if (( status != 0 )) || [[ "${top}" != yes ]]; then
    failed=1
  fi
  return 0
}

cd "${work}" || exit 1

run_logged tool_versions kompile --version
run_logged function_ast \
  python3 /audit-output/evidence/check_function_ast.py \
  "${work}/solution.py" /audit-output/evidence/concrete_smoke.py

concrete_mpy="${work}/concrete-smoke.mpy"
out="${log_dir}/translate_concrete.log"
printf 'COMMAND: python3 %q %q > %q\n' \
  "${work}/py2mpy.py" /audit-output/evidence/concrete_smoke.py \
  "${concrete_mpy}" >"${out}"
python3 "${work}/py2mpy.py" /audit-output/evidence/concrete_smoke.py \
  >"${concrete_mpy}" 2>>"${out}"
status=$?
printf 'EXIT_STATUS: %s\n' "${status}" >>"${out}"
printf 'translate_concrete EXIT_STATUS=%s LOG=%s\n' "${status}" "${out}" \
  >>"${summary}"
if (( status != 0 )); then failed=1; fi

run_logged build_runtime \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
run_logged run_submitted_module \
  krun solution.mpy --definition runtime-kompiled
run_logged run_concrete_smoke \
  krun concrete-smoke.mpy --definition runtime-kompiled

run_logged build_verification_base \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-BASE \
  --output-definition verification-base-kompiled
run_proof prove_loop \
  kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC

run_logged build_verification \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
run_proof prove_entry \
  kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

printf 'OVERALL_EXIT_STATUS: %s\n' "${failed}" >>"${summary}"
exit "${failed}"
