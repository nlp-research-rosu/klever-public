#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_shell 'find /audit-output/evidence -maxdepth 1 -type f -printf "%f %s bytes\\n" | LC_ALL=C sort'
run_shell 'sha256sum /audit-output/evidence/*.py /audit-output/evidence/*.k /audit-output/evidence/*.sh | LC_ALL=C sort -k2'
run_shell 'find /tmp/audit-work/audit-119-match-parens -maxdepth 1 -type d -name "*-kompiled" -printf "%f\\n" | LC_ALL=C sort'
