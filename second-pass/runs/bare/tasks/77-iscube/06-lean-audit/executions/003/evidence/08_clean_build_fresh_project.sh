#!/usr/bin/env bash
set -euo pipefail
set -x

export LD_PRELOAD=/tmp/audit-work/lean-proc-exe-compat.so
cd /tmp/audit-work/77-iscube-proof-audit
lake clean
lake build
