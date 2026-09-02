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

printf 'STAGE 5 REAL-PROGRAM BODY-SENSITIVITY CHECK\n'
run python3 "$evidence_dir/make_body_mutation.py" \
  "$source_dir/solution.py" /tmp/audit-work/mutated-solution.py

printf '$ python3 /reference/py2mpy.py /tmp/audit-work/mutated-solution.py > /tmp/audit-work/mutated-solution.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/mutated-solution.py > /tmp/audit-work/mutated-solution.mpy
printf 'EXIT_STATUS=%d\n' "$?"

printf '$ cmp /tmp/audit-work/mutated-solution.mpy %q\n' "$source_dir/solution.mpy"
cmp /tmp/audit-work/mutated-solution.mpy "$source_dir/solution.mpy"
printf 'EXIT_STATUS=%d\n' "$?"

run python3 "$evidence_dir/body_mutation_check.py" \
  /reference/canonical.py /tmp/audit-work/mutated-solution.py

# No proof input is changed: this is deliberately the submitted proof against
# the now-materially-different program artifact in the same scratch audit.
run kprove "$source_dir/spec.k" \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC \
  --claims loop
