#!/usr/bin/env bash
set -euo pipefail

source_file=/audit-output/evidence/04a_hostpid_preload.c
shared_object=/tmp/audit-work/lean-hostpid-preload.so
lean_root=/opt/elan/toolchains/leanprover--lean4---v4.22.0

echo '$ gcc -shared -fPIC -O2 -o /tmp/audit-work/lean-hostpid-preload.so 04a_hostpid_preload.c'
gcc -shared -fPIC -O2 -o "$shared_object" "$source_file"
echo '$ LD_PRELOAD=lean-hostpid-preload.so python3 (compare namespace and procfs PID)'
LD_PRELOAD="$shared_object" python3 - <<'PY'
import os
pid = os.getpid()
print("getpid:", pid)
print("proc status:", next(line for line in open("/proc/self/status") if line.startswith("Pid:")).strip())
print("resolved executable:", os.readlink(f"/proc/{pid}/exe"))
PY
echo '$ LD_PRELOAD=lean-hostpid-preload.so lean --version'
LD_PRELOAD="$shared_object" "$lean_root/bin/lean" --version
echo '$ LD_PRELOAD=lean-hostpid-preload.so lake --version'
LD_PRELOAD="$shared_object" "$lean_root/bin/lake" --version
