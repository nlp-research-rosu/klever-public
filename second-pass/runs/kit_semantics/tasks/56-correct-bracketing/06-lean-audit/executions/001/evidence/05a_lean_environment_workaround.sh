#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

shim_dir=/tmp/audit-work/lean-proc-shim
mkdir -p "$shim_dir"

printf 'COMMAND: demonstrate namespace PID versus host /proc PID\n'
python - <<'PY'
import os
print(f'getpid={os.getpid()}')
print(f'/proc/self symlink={os.readlink("/proc/self")}')
pid_path = f'/proc/{os.getpid()}/exe'
print(f'{pid_path} exists={os.path.exists(pid_path)}')
print(f'/proc/self/exe={os.readlink("/proc/self/exe")}')
PY

printf '\nCOMMAND: compile the narrow getpid compatibility shim\n'
cc -shared -fPIC -O2 \
  /audit-output/evidence/lean_proc_pid_shim.c \
  -o "$shim_dir/lean_proc_pid_shim.so"
sha256sum \
  /audit-output/evidence/lean_proc_pid_shim.c \
  "$shim_dir/lean_proc_pid_shim.so"

printf '\nCOMMAND: show Lean failure without shim (expected infrastructure failure)\n'
set +o errexit
/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
without_status=$?
set -o errexit
printf 'without_shim_exit=%s\n' "$without_status"

printf '\nCOMMAND: show pinned Lean succeeds with shim\n'
LD_PRELOAD="$shim_dir/lean_proc_pid_shim.so" \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version

printf '\nCOMMAND: show pinned Lake succeeds with complete existing toolchain paths and shim\n'
LD_PRELOAD="$shim_dir/lean_proc_pid_shim.so" \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LEAN=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean \
LAKE=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake --version
