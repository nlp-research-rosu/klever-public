#!/usr/bin/env bash
set -u
shim=/tmp/audit-work/proc_self_readlink_shim.so
echo '$ cc -shared -fPIC -O2 -Wall -Wextra -o /tmp/audit-work/proc_self_readlink_shim.so /audit-output/evidence/proc_self_readlink_shim.c'
cc -shared -fPIC -O2 -Wall -Wextra \
  -o "$shim" \
  /audit-output/evidence/proc_self_readlink_shim.c
echo '$ sha256sum /audit-output/evidence/proc_self_readlink_shim.c /tmp/audit-work/proc_self_readlink_shim.so'
sha256sum \
  /audit-output/evidence/proc_self_readlink_shim.c \
  "$shim"
echo '$ python3 -c (show namespace PID and failing /proc/PID/exe)'
python3 -c 'import os; p=f"/proc/{os.getpid()}/exe"; print("pid", os.getpid(), "path", p, "exists", os.path.exists(p))'
echo '$ LD_PRELOAD=... /opt/elan/bin/lean --version'
LD_PRELOAD="$shim" /opt/elan/bin/lean --version
echo '$ LD_PRELOAD=... /opt/elan/bin/lean --print-prefix'
LD_PRELOAD="$shim" /opt/elan/bin/lean --print-prefix
echo '$ LD_PRELOAD=... /opt/elan/bin/lake --version'
LD_PRELOAD="$shim" /opt/elan/bin/lake --version
