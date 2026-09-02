#!/usr/bin/env bash
set -u

printf 'shell_pid=%s\n' "$$"
readlink /proc/self/exe
readlink "/proc/$$/exe"
printf 'pid_named_readlink_exit=%s\n' "$?"
lean --version
printf 'unadjusted_lean_exit=%s\n' "$?"
objdump -d \
  --start-address=0x73c4a70 \
  --stop-address=0x73c4b50 \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/lib/lean/libleanshared.so
LD_PRELOAD=/tmp/audit-work/lean_app_path_compat.so lean --version
printf 'compat_lean_exit=%s\n' "$?"
