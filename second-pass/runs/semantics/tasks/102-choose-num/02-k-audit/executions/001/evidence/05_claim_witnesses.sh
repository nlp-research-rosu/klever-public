#!/usr/bin/env bash
set +e

printf 'Stage 4 satisfiable entry witnesses and ground result substitutions\n'
printf '\n$ python3 /audit-output/evidence/claim_witnesses.py\n'
python3 /audit-output/evidence/claim_witnesses.py
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
