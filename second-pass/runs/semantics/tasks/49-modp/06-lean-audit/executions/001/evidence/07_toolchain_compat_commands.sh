#!/usr/bin/env bash
set -eu

printf 'namespace_pid=%s\n' "$$"
set +e
readlink "/proc/$$/exe"
numeric_proc_status=$?
lean --version
unshimmed_lean_status=$?
set -e
printf 'numeric_proc_exe_status=%s\n' "${numeric_proc_status}"
printf 'unshimmed_lean_status=%s\n' "${unshimmed_lean_status}"

printf '%s\n' '$ compatibility shim identity and repaired toolchain identity'
sha256sum \
  /audit-output/evidence/proc_exe_compat.c \
  /tmp/audit-work/proc_exe_compat.so
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lean --version
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake --version
