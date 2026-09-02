#!/usr/bin/env bash
set +e

printf 'Stage 4 exact submitted-body pinning check\n'
printf '\n$ python3 /audit-output/evidence/program_pinning.py\n'
python3 /audit-output/evidence/program_pinning.py
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
