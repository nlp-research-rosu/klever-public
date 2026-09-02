#!/usr/bin/env bash
set -u

echo "Diagnostic: sandbox PID and proc visibility"
python3 -c 'import os; p=f"/proc/{os.getpid()}/exe"; print("getpid_path", p); print("getpid_path_exists", os.path.exists(p)); print("self_exe", os.readlink("/proc/self/exe"))'

echo "Pinned Lean without the narrow proc shim (expected sandbox-only startup failure)"
/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
echo "unshimmed_exit=$?"

echo "Compile the readlink shim used for the successful preflight"
cc -shared -fPIC \
  /audit-output/evidence/proc-self-readlink-shim.c \
  -ldl \
  -o /tmp/audit-work/proc-self-readlink-shim.so
echo "shim_compile_exit=$?"

echo "Pinned Lean with the narrow proc shim"
LD_PRELOAD=/tmp/audit-work/proc-self-readlink-shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
echo "shimmed_exit=$?"
