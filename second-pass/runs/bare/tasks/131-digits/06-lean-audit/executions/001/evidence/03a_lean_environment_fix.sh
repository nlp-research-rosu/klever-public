#!/usr/bin/env bash
set -euxo pipefail

gcc \
  -shared \
  -fPIC \
  -O2 \
  -Wall \
  -Wextra \
  -o /tmp/audit-work/lean_app_path_shim.so \
  /audit-output/evidence/lean_app_path_shim.c \
  -ldl
sha256sum /audit-output/evidence/lean_app_path_shim.c
sha256sum /tmp/audit-work/lean_app_path_shim.so
LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so lake --version
