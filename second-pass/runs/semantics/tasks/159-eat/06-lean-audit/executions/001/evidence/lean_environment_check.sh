#!/usr/bin/env bash
set -u

echo '$ sed -n "/^Pid:/p; /^NSpid:/p" /proc/self/status'
sed -n -e '/^Pid:/p' -e '/^NSpid:/p' /proc/self/status

echo '$ lean --version'
lean --version
uncorrected_exit=$?
echo "uncorrected_exit=$uncorrected_exit"

echo '$ cc -shared -fPIC -O2 -Wall -Wextra evidence/outer_pid_preload.c -o /tmp/audit-work/outer_pid_preload.so'
cc -shared -fPIC -O2 -Wall -Wextra \
    evidence/outer_pid_preload.c \
    -o /tmp/audit-work/outer_pid_preload.so
compile_exit=$?
echo "compile_exit=$compile_exit"

echo '$ LD_PRELOAD=/tmp/audit-work/outer_pid_preload.so lean --version'
LD_PRELOAD=/tmp/audit-work/outer_pid_preload.so lean --version
corrected_lean_exit=$?
echo "corrected_lean_exit=$corrected_lean_exit"

echo '$ LD_PRELOAD=/tmp/audit-work/outer_pid_preload.so lake --version'
LD_PRELOAD=/tmp/audit-work/outer_pid_preload.so lake --version
corrected_lake_exit=$?
echo "corrected_lake_exit=$corrected_lake_exit"

if (( compile_exit != 0 || corrected_lean_exit != 0 || corrected_lake_exit != 0 )); then
    exit 1
fi
