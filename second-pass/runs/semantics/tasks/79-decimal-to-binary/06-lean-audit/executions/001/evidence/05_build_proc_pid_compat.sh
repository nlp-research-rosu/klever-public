#!/usr/bin/env bash
set -euo pipefail

echo '$ cc -shared -fPIC -O2 -Wall -Wextra -Werror -o /tmp/audit-work/proc_pid_compat.so /audit-output/evidence/proc_pid_compat.c'
cc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc_pid_compat.so \
  /audit-output/evidence/proc_pid_compat.c

echo '$ sha256sum /audit-output/evidence/proc_pid_compat.c /tmp/audit-work/proc_pid_compat.so'
sha256sum /audit-output/evidence/proc_pid_compat.c /tmp/audit-work/proc_pid_compat.so

echo '$ LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version'
LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version

echo '$ LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --print-prefix'
LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --print-prefix
