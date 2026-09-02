#!/usr/bin/env bash
set -u

work="/tmp/audit-work/reconstruction"
log="/audit-output/evidence/fidelity.log"
: >"${log}"

run() {
  printf 'COMMAND: %s\n' "$*" >>"${log}"
  "$@" >>"${log}" 2>&1
  status=$?
  printf 'EXIT_STATUS: %s\n\n' "${status}" >>"${log}"
  return "${status}"
}

run python3 "${work}/py2mpy.py" "${work}/solution.py"
translate_status=$?

# Regenerate to a fresh file for a byte-for-byte comparison with the submitted
# constructor program.
printf 'COMMAND: python3 %s/py2mpy.py %s/solution.py > %s/solution.regenerated.mpy\n' \
  "${work}" "${work}" "${work}" >>"${log}"
python3 "${work}/py2mpy.py" "${work}/solution.py" \
  >"${work}/solution.regenerated.mpy" 2>>"${log}"
regen_status=$?
printf 'EXIT_STATUS: %s\n\n' "${regen_status}" >>"${log}"

run cmp -s "${work}/solution.regenerated.mpy" "${work}/solution.mpy"
cmp_status=$?
run sha256sum "${work}/solution.regenerated.mpy" "${work}/solution.mpy"
hash_status=$?
run python3 /audit-output/evidence/differential_test.py \
  "${work}/canonical.py" "${work}/solution.py"
diff_status=$?

if (( translate_status || regen_status || cmp_status || hash_status || diff_status )); then
  exit 1
fi
