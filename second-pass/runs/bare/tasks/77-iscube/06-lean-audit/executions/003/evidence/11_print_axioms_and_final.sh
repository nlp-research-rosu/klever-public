#!/usr/bin/env bash
set -euo pipefail
set -x

export LD_PRELOAD=/tmp/audit-work/lean-proc-exe-compat.so
cd /tmp/audit-work/77-iscube-proof-audit
lake env lean Axioms.lean
lake env lean PrintFinal.lean
