#!/usr/bin/env bash
set -uo pipefail
trap 'rc=$?; printf "\nSCRIPT_EXIT_CODE=%s\n" "$rc"' EXIT

command -v lake
command -v lean

lake --version
printf 'LAKE_VERSION_EXIT_CODE=%s\n' "$?"

lean --version
printf 'LEAN_VERSION_EXIT_CODE=%s\n' "$?"

python3 -c '
import os
print("pid", os.getpid())
print("proc_self_exe", os.readlink("/proc/self/exe"))
print("numeric_proc_exe_exists", os.path.exists(f"/proc/{os.getpid()}/exe"))
'
printf 'PROC_DIAGNOSTIC_EXIT_CODE=%s\n' "$?"
