#!/usr/bin/env bash
set -u

pwd
printenv AUDIT_MODE
ls -ld /audit-input.json /audit-output/audit-input.json /candidate 2>&1 || true
find /reference /candidate -maxdepth 3 -type f -printf '%p\n' 2>&1 | sort
python3 -m json.tool /audit-input.json
