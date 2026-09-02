#!/usr/bin/env bash
set -euo pipefail

gcc -shared -fPIC -O2 \
  -o /tmp/audit-work/lean-proc-exe-compat.so \
  /audit-output/evidence/lean_proc_exe_compat.c
sha256sum \
  /audit-output/evidence/lean_proc_exe_compat.c \
  /tmp/audit-work/lean-proc-exe-compat.so
LD_PRELOAD=/tmp/audit-work/lean-proc-exe-compat.so lean --version
LD_PRELOAD=/tmp/audit-work/lean-proc-exe-compat.so lake --version
