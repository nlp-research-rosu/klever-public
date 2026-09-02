#!/usr/bin/env bash
set -u

log="/audit-output/evidence/provenance-large-untrusted.log"
exec >"$log" 2>&1

printf '$ python3 /audit-output/evidence/summarize_untrusted_generation.py\n'
python3 /audit-output/evidence/summarize_untrusted_generation.py
status=$?
printf '[exit %d]\n' "$status"
