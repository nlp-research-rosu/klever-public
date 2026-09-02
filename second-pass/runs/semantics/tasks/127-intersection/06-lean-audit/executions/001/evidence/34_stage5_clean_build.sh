#!/usr/bin/env bash
set -u

audit_root=/tmp/audit-work/stage5-proof-audit
compat_so=/tmp/audit-work/proc_exe_compat.so

cd "$audit_root" || exit 97

echo '$ LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake clean'
LD_PRELOAD="$compat_so" lake clean
clean_status=$?
echo "lake_clean_exit=$clean_status"

echo '$ LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake build'
LD_PRELOAD="$compat_so" lake build
build_status=$?
echo "lake_build_exit=$build_status"

if [ "$clean_status" -ne 0 ] || [ "$build_status" -ne 0 ]; then
  exit 1
fi
