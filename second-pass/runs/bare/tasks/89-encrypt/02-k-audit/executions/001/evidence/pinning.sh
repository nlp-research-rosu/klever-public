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

cd /tmp/audit-work/source || exit 99

echo "Trusted regeneration:"
printf '$ python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy\n'
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
regen_status=$?
printf '[exit %d]\n' "$regen_status"
run cmp -s regenerated-solution.mpy solution.mpy
mpy_cmp=$?

echo "Normalize actual parsed body and solutionBody abbreviation through the module-entry step:"
echo "\$ krun solution.mpy -cINPUT='\"\"' --definition /tmp/audit-work/build/proof-kompiled --parser /audit-output/evidence/mpy-full-parser.sh --depth 1 > /tmp/audit-work/build/actual-depth0.txt"
krun solution.mpy \
  -cINPUT='""' \
  --definition /tmp/audit-work/build/proof-kompiled \
  --parser /audit-output/evidence/mpy-full-parser.sh \
  --depth 1 > /tmp/audit-work/build/actual-depth0.txt
actual_status=$?
printf '[exit %d]\n' "$actual_status"

echo "\$ krun solution-symbolic.mpy -cINPUT='\"\"' --definition /tmp/audit-work/build/proof-kompiled --parser /audit-output/evidence/mpy-full-parser.sh --depth 1 > /tmp/audit-work/build/symbolic-depth0.txt"
krun solution-symbolic.mpy \
  -cINPUT='""' \
  --definition /tmp/audit-work/build/proof-kompiled \
  --parser /audit-output/evidence/mpy-full-parser.sh \
  --depth 1 > /tmp/audit-work/build/symbolic-depth0.txt
symbolic_status=$?
printf '[exit %d]\n' "$symbolic_status"

run cmp -s \
  /tmp/audit-work/build/actual-depth0.txt \
  /tmp/audit-work/build/symbolic-depth0.txt
config_cmp=$?
run sha256sum \
  /tmp/audit-work/build/actual-depth0.txt \
  /tmp/audit-work/build/symbolic-depth0.txt

echo "Concrete satisfying substitutions:"
run python3 - <<'PY'
from canonical import encrypt as canonical
from solution import encrypt as generated

for value in ["", "hi", "A", "🙂"]:
    print(repr(value), "canonical=", repr(canonical(value)), "generated=", repr(generated(value)))
PY
substitution_status=$?

printf 'summary regen=%d mpy_cmp=%d actual=%d symbolic=%d config_cmp=%d substitutions=%d\n' \
  "$regen_status" "$mpy_cmp" "$actual_status" "$symbolic_status" "$config_cmp" "$substitution_status"
if (( regen_status || mpy_cmp || actual_status || symbolic_status || config_cmp || substitution_status )); then
  exit 1
fi
