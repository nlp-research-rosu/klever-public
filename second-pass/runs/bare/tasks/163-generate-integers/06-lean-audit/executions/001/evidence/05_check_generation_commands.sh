#!/usr/bin/env bash
set -uo pipefail
trap 'rc=$?; printf "\nEXIT_CODE=%s\n" "$rc"' EXIT

cc -shared -fPIC \
  /audit-output/evidence/05_proc_exe_compat.c \
  -o /tmp/audit-work/05_proc_exe_compat.so \
  -ldl

LD_PRELOAD=/tmp/audit-work/05_proc_exe_compat.so \
PYTHONPATH=/reference python3 \
  /audit-output/evidence/05_check_generation.py
