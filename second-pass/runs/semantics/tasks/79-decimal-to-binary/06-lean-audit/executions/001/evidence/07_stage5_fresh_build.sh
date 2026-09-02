#!/usr/bin/env bash
set -euo pipefail

audit_stage5_dir=/tmp/audit-work/stage5-fresh
if [[ -e "$audit_stage5_dir" ]]; then
  echo "refusing to reuse non-fresh path: $audit_stage5_dir" >&2
  exit 97
fi

echo '$ mkdir -p /tmp/audit-work/stage5-fresh'
mkdir -p "$audit_stage5_dir"

echo '$ cp -a /candidate/. /tmp/audit-work/stage5-fresh/'
cp -a /candidate/. "$audit_stage5_dir/"

echo '$ cp -a /reference/klean-generation/generated/. /tmp/audit-work/stage5-fresh/Base/'
cp -a /reference/klean-generation/generated/. "$audit_stage5_dir/Base/"

echo '$ export ELAN_HOME=/opt/elan'
export ELAN_HOME=/opt/elan
echo '$ export LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so'
export LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so

echo '$ cd /tmp/audit-work/stage5-fresh'
cd "$audit_stage5_dir"

echo '$ lake clean'
lake clean

echo '$ lake build'
lake build
