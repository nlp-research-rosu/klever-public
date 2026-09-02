#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/proof || exit 90
audit_definition=/tmp/audit-work/proof/audit-haskell-kompiled

printf 'COMMAND: krun solution.mpy --definition %s -cINPUT=%q --depth 1 --output kore\n' \
  "$audit_definition" '"<>"'
krun solution.mpy \
  --definition "$audit_definition" \
  -cINPUT='"<>"' \
  --depth 1 \
  --output kore \
  > solution-body.kore \
  2> solution-body.err
solution_exit=$?
printf 'solution depth-limited execution exit=%s\n' "$solution_exit"
sed -n '1,40p' solution-body.err

printf 'COMMAND: krun correct-program.mpy --definition %s -cINPUT=%q --depth 2 --output kore\n' \
  "$audit_definition" '"<>"'
krun correct-program.mpy \
  --definition "$audit_definition" \
  -cINPUT='"<>"' \
  --depth 2 \
  --output kore \
  > correct-body.kore \
  2> correct-body.err
macro_exit=$?
printf 'correctProgram depth-limited execution exit=%s\n' "$macro_exit"
sed -n '1,40p' correct-body.err

sha256sum solution-body.kore correct-body.kore
cmp -s solution-body.kore correct-body.kore
cmp_exit=$?
printf 'constructor-level post-expansion state cmp exit=%s\n' "$cmp_exit"

python3 /audit-output/evidence/adequacy_witnesses.py
witness_exit=$?
printf 'adequacy witnesses exit=%s\n' "$witness_exit"

if (( solution_exit != 0 || macro_exit != 0 || cmp_exit != 0 || witness_exit != 0 )); then
  exit 1
fi
