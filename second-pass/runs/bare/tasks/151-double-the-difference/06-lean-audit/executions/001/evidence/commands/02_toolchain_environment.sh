#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

python3 -c 'import os; print("getpid", os.getpid()); print("/proc/self", os.readlink("/proc/self")); print("/proc/self/exe", os.readlink("/proc/self/exe"))'
lean --version || true
lake --version
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc_pid_shim.so \
  /audit-output/evidence/commands/proc_pid_shim.c
env LD_PRELOAD=/tmp/audit-work/proc_pid_shim.so lean --version
env LD_PRELOAD=/tmp/audit-work/proc_pid_shim.so lake --version
