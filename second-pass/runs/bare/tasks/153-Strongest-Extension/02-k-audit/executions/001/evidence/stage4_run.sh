#!/usr/bin/env bash
set -u
status=0

echo '$ python3 /audit-output/evidence/stage4_claim_witnesses.py'
python3 /audit-output/evidence/stage4_claim_witnesses.py
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ submitted MPY and proof macro KORE identity (recheck)'
cmp -s /tmp/audit-work/submitted.kore /tmp/audit-work/macro.kore
rc=$?
echo "cmp_exit=$rc"
(( rc == 0 )) || status=1
sha256sum /tmp/audit-work/submitted.kore /tmp/audit-work/macro.kore
rc=$?
echo "sha256sum_exit=$rc"
(( rc == 0 )) || status=1

echo "stage4_exit=$status"
exit "$status"
