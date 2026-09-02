#!/usr/bin/env bash
set -euo pipefail
set -x

gcc -shared -fPIC -O2 \
  /audit-output/evidence/proc_pid_shim.c \
  -o /tmp/audit-work/proc_pid_shim.so

sha256sum \
  /audit-output/evidence/proc_pid_shim.c \
  /tmp/audit-work/proc_pid_shim.so

LD_PRELOAD=/tmp/audit-work/proc_pid_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/proc_pid_shim.so lake --version
