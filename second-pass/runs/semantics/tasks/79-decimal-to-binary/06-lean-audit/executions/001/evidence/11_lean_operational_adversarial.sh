#!/usr/bin/env bash
set -euo pipefail

export ELAN_HOME=/opt/elan
export LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so

echo '$ cd /tmp/audit-work/stage5-fresh'
cd /tmp/audit-work/stage5-fresh

echo '$ lake env lean OperationalAudit.lean'
lake env lean OperationalAudit.lean
