#!/usr/bin/env bash
set -euo pipefail

program=/tmp/audit-work/104-unique-digits/candidate/solution.mpy
definition=/tmp/audit-work/104-unique-digits/candidate/semantic-audit-kompiled

/audit-output/evidence/run_logged.sh stage3_krun_empty \
  krun "$program" --definition "$definition" \
  -cARGS='pyList(.Ints)'

/audit-output/evidence/run_logged.sh stage3_krun_base_and_even \
  krun "$program" --definition "$definition" \
  -cARGS='pyList(cons(1, cons(2, .Ints)))'

/audit-output/evidence/run_logged.sh stage3_krun_example_one \
  krun "$program" --definition "$definition" \
  -cARGS='pyList(cons(15, cons(33, cons(1422, cons(1, .Ints)))))'

/audit-output/evidence/run_logged.sh stage3_krun_example_two \
  krun "$program" --definition "$definition" \
  -cARGS='pyList(cons(152, cons(323, cons(1422, cons(10, .Ints)))))'

/audit-output/evidence/run_logged.sh stage3_krun_duplicates \
  krun "$program" --definition "$definition" \
  -cARGS='pyList(cons(97531, cons(7, cons(111, cons(97531, .Ints)))))'
