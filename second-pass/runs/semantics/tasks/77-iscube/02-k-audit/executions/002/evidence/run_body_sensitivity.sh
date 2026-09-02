#!/usr/bin/env bash
set -uo pipefail

mutation_dir=/tmp/audit-work/body-sensitivity
overall=0

if [[ -e "$mutation_dir" ]]; then
  printf 'ERROR: preexisting mutation directory: %s\n' "$mutation_dir"
  exit 98
fi

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
}

run mkdir -p "$mutation_dir"
run cp -a /tmp/audit-work/candidate/reference-semantics "$mutation_dir/"
run cp /tmp/audit-work/candidate/spec.k "$mutation_dir/spec.k"
run cp /tmp/audit-work/candidate/verification.k "$mutation_dir/verification.k"
run cp /audit-output/evidence/body_mutation_solution.py "$mutation_dir/solution.py"

cd "$mutation_dir" || exit 99

printf '%s\n' 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py solution.py > solution.mpy'
python3 /tmp/audit-work/trusted/py2mpy.py solution.py > solution.mpy
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
if (( status != 0 )); then
  overall=1
fi

printf '%s\n' 'COMMAND: sed -i 73s/Int(1)/Int(2)/ verification.k'
sed -i '73s/Int(1)/Int(2)/' verification.k
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
if (( status != 0 )); then
  overall=1
fi

run python3 /audit-output/evidence/constructor_compare.py \
  --solution "$mutation_dir/solution.mpy" \
  --verification "$mutation_dir/verification.k"

run kompile verification.k \
  --backend haskell \
  --main-module ISCube-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mut-kompiled \
  -I .

printf '%s\n' 'COMMAND (expected stuck proof): kprove spec.k --definition verification-body-mut-kompiled --spec-module ISCube-SPEC --claims ISCube-SPEC.positive-cubes --output pretty --warnings all'
kprove spec.k \
  --definition verification-body-mut-kompiled \
  --spec-module ISCube-SPEC \
  --claims ISCube-SPEC.positive-cubes \
  --output pretty \
  --warnings all
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
if (( status == 0 )); then
  overall=1
fi

exit "$overall"
