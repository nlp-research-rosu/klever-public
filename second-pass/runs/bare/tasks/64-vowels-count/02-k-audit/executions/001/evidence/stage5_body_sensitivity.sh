#!/usr/bin/env bash
set -u
set -x

python3 /reference/py2mpy.py \
  /audit-output/evidence/solution-body-mutated.py \
  > /tmp/audit-work/solution-body-mutated.mpy
translator_exit=$?
kast \
  /tmp/audit-work/solution-body-mutated.mpy \
  --definition /tmp/audit-work/verification-fresh-kompiled \
  --module MPY-SYNTAX \
  --sort Program \
  --expand-macros \
  --output kore \
  --output-file /tmp/audit-work/mutated-expanded.kore
kast_exit=$?
cmp --silent \
  /tmp/audit-work/mutated-expanded.kore \
  /tmp/audit-work/macro-expanded.kore
mutated_macro_cmp_exit=$?
krun \
  /tmp/audit-work/solution-body-mutated.mpy \
  --definition /tmp/audit-work/semantic-fresh-kompiled \
  -cINPUT='""' \
  --output pretty \
  > /tmp/audit-work/mutated-empty.krun.out
krun_exit=$?
sed -n '/<k>/,/<\/k>/p' /tmp/audit-work/mutated-empty.krun.out
printf 'translator_exit=%s\n' "$translator_exit"
printf 'kast_exit=%s\n' "$kast_exit"
printf 'mutated_macro_cmp_exit=%s (expected nonzero)\n' "$mutated_macro_cmp_exit"
printf 'krun_exit=%s\n' "$krun_exit"
test "$translator_exit" -eq 0
test "$kast_exit" -eq 0
test "$mutated_macro_cmp_exit" -ne 0
test "$krun_exit" -eq 0
grep -Eq 'intVal\s*\(\s*9\s*\)' /tmp/audit-work/mutated-empty.krun.out
