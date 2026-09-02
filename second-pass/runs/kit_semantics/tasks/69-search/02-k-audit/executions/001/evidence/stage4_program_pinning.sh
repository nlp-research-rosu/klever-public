#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/reconstruction
status=0

python3 /audit-output/evidence/extract_spec_program.py
extract_exit=$?
printf 'extract_exit=%s\n' "$extract_exit"
if [[ "$extract_exit" != 0 ]]; then
  status=1
fi

kast solution.mpy \
  --definition audit-verification-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --output kore \
  --output-file /tmp/audit-work/reconstruction/solution_program.kore
solution_kast_exit=$?
printf 'solution_kast_exit=%s\n' "$solution_kast_exit"
if [[ "$solution_kast_exit" != 0 ]]; then
  status=1
fi

kast spec_program.mpy \
  --definition audit-verification-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --output kore \
  --output-file /tmp/audit-work/reconstruction/spec_program.kore
spec_kast_exit=$?
printf 'spec_kast_exit=%s\n' "$spec_kast_exit"
if [[ "$spec_kast_exit" != 0 ]]; then
  status=1
fi

sha256sum solution_program.kore spec_program.kore
cmp -s solution_program.kore spec_program.kore
constructor_compare_exit=$?
printf 'constructor_kore_cmp_exit=%s\n' "$constructor_compare_exit"
if [[ "$constructor_compare_exit" != 0 ]]; then
  diff -u solution_program.kore spec_program.kore | head -200
  status=1
fi

printf 'stage4_program_pinning_exit=%s\n' "$status"
exit "$status"
