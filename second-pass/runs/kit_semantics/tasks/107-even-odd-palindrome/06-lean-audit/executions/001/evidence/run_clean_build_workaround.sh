#!/usr/bin/env bash
set -u

shim_source=/tmp/audit-work/proc-self-shim.c
shim_library=/tmp/audit-work/proc-self-shim.so
lean_sysroot=/opt/elan/toolchains/leanprover--lean4---v4.22.0
scratch=$(mktemp -d /tmp/audit-work/lean-sandbox-evidence.XXXXXX)
project="$scratch/project"

cp -a /reference/klean-generation/generated "$project"
cd "$project"

printf 'sandbox_shell_pid=%s\n' "$$"
if [ -e "/proc/$$/exe" ]; then
    printf 'sandbox_pid_proc_entry=present\n'
else
    printf 'sandbox_pid_proc_entry=absent\n'
fi

printf 'COMMAND: lake --version\n'
lake --version
printf 'COMMAND: lake clean (expected sandbox installation-detection failure)\n'
lake clean
unshimmed_exit=$?
printf 'unshimmed_lake_clean_exit=%s\n' "$unshimmed_exit"

printf 'COMMAND: cc -shared -fPIC -O2 -Wall -Wextra -Werror -o %s %s -ldl\n' \
    "$shim_library" "$shim_source"
cc -shared -fPIC -O2 -Wall -Wextra -Werror \
    -o "$shim_library" "$shim_source" -ldl
sha256sum "$shim_source" "$shim_library"

export LD_PRELOAD="$shim_library"
printf 'COMMAND: lean --version (with proc-self shim)\n'
lean --version
printf 'COMMAND: lake clean (with proc-self shim)\n'
lake clean
printf 'shimmed_lake_clean_exit=%s\n' "$?"
printf 'COMMAND: lake build (with proc-self shim)\n'
lake build
printf 'shimmed_lake_build_exit=%s\n' "$?"
printf 'pinned_lean_sysroot=%s\n' "$lean_sysroot"
