#!/usr/bin/env bash
set -u

printf '$ python3 /audit-output/evidence/07-import-model-witness.py\n'
python3 /audit-output/evidence/07-import-model-witness.py
status=$?
printf '[exit %d]\n' "$status"

printf '\nK comparison location: 03-reconstruct.log lines 88-144.\n'
printf 'That final <scopes> cell contains all_prefixes but no List binding.\n'
exit "$status"

