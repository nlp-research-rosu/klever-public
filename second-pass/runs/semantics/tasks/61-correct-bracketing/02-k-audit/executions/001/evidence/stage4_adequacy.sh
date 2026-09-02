#!/usr/bin/env bash
set +e

source_dir=/tmp/audit-work/candidate-src
evidence_dir=/audit-output/evidence

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS=%d\n' "$rc"
  return "$rc"
}

printf 'STAGE 4 ADEQUACY AND REAL-PROGRAM PINNING\n'
run python3 "$evidence_dir/make_k_smoke.py" \
  "$source_dir/solution.py" /tmp/audit-work/concrete-smoke.py

printf '$ python3 /reference/py2mpy.py /tmp/audit-work/concrete-smoke.py > /tmp/audit-work/concrete-smoke.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/concrete-smoke.py > /tmp/audit-work/concrete-smoke.mpy
printf 'EXIT_STATUS=%d\n' "$?"

run krun /tmp/audit-work/concrete-smoke.mpy \
  --definition /tmp/audit-work/build/runtime-kompiled

run python3 "$evidence_dir/claim_witnesses.py" \
  /reference/canonical.py "$source_dir/solution.py"

printf '$ rg -n %q %q %q\n' \
  'solution[.]mpy|correct_bracketing|#loadAll|Module\\(|Call\\(' \
  "$source_dir/spec.k" "$source_dir/verification.k"
rg -n 'solution[.]mpy|correct_bracketing|#loadAll|Module\(|Call\(' \
  "$source_dir/spec.k" "$source_dir/verification.k"
printf 'EXIT_STATUS=%d\n' "$?"

printf '$ rg -n %q %q\n' \
  '#loop|Return\\(Compare\\(Name\\(\"balance\"\\)' "$source_dir/spec.k"
rg -n '#loop|Return\(Compare\(Name\("balance"\)' "$source_dir/spec.k"
printf 'EXIT_STATUS=%d\n' "$?"
