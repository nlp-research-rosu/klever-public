#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/35-max-element-proof-audit
export LD_PRELOAD=/tmp/audit-work/proc_pid_shim.so
lake env lean /audit-output/evidence/PrintAxioms.lean
