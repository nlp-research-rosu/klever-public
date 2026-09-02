#!/bin/sh
set -eu

gcc -shared -fPIC /audit-output/evidence/procself_readlink_shim.c \
  -ldl -o /tmp/audit-work/libprocself_readlink.so
LD_PRELOAD=/tmp/audit-work/libprocself_readlink.so \
  PYTHONPATH=/reference \
  python /audit-output/evidence/rerun_preflight.py
