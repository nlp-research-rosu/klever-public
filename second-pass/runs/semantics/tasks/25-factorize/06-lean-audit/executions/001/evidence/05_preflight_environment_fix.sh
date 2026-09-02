#!/usr/bin/env bash
set -uo pipefail

echo '$ gcc -shared -fPIC -o /tmp/audit-work/proc_self_exe_compat.so /audit-output/evidence/proc_self_exe_compat.c -ldl'
gcc -shared -fPIC \
  -o /tmp/audit-work/proc_self_exe_compat.so \
  /audit-output/evidence/proc_self_exe_compat.c \
  -ldl
compile_rc=$?
echo "exit_code=$compile_rc"
if [ "$compile_rc" -ne 0 ]; then
  exit "$compile_rc"
fi

echo '$ LD_PRELOAD=/tmp/audit-work/proc_self_exe_compat.so lean --version'
LD_PRELOAD=/tmp/audit-work/proc_self_exe_compat.so lean --version
lean_rc=$?
echo "exit_code=$lean_rc"

echo '$ LD_PRELOAD=/tmp/audit-work/proc_self_exe_compat.so lake --version'
LD_PRELOAD=/tmp/audit-work/proc_self_exe_compat.so lake --version
lake_rc=$?
echo "exit_code=$lake_rc"

if [ "$lean_rc" -ne 0 ]; then
  exit "$lean_rc"
fi
exit "$lake_rc"
