#!/usr/bin/env bash
set -euo pipefail

printf -v deep_positive '%*s' 1200 ''
deep_positive=${deep_positive// /1}
arguments="pyList(cons(${deep_positive}, .Ints))"

printf 'WITNESS_CONSTRUCTION: int("1" repeated 1200 times)\n'
printf 'WITNESS_IS_POSITIVE: yes\n'
/audit-output/evidence/run_logged.sh stage4_krun_deep_positive \
  krun /tmp/audit-work/104-unique-digits/candidate/solution.mpy \
    --definition /tmp/audit-work/104-unique-digits/candidate/semantic-audit-kompiled \
    "-cARGS=${arguments}"
