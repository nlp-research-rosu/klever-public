#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' \
  'COMMAND: cc -O2 -Wall -Wextra -Werror 05_app_path_probe.c -o /tmp/audit-work/app_path_probe'
cc -O2 -Wall -Wextra -Werror \
  /audit-output/evidence/05_app_path_probe.c \
  -o /tmp/audit-work/app_path_probe
printf '%s\n' \
  'COMMAND: cc -shared -fPIC -O2 -Wall -Wextra -Werror -ldl 05_proc_exe_compat.c -o /tmp/audit-work/05_proc_exe_compat.so'
cc -shared -fPIC -O2 -Wall -Wextra -Werror \
  /audit-output/evidence/05_proc_exe_compat.c \
  -ldl \
  -o /tmp/audit-work/05_proc_exe_compat.so
printf '%s\n' 'COMMAND: sha256sum compatibility shim source and binary'
sha256sum \
  /audit-output/evidence/05_app_path_probe.c \
  /tmp/audit-work/app_path_probe \
  /audit-output/evidence/05_proc_exe_compat.c \
  /tmp/audit-work/05_proc_exe_compat.so
printf '%s\n' 'COMMAND: unshimmed application-path probe (expected environment failure)'
set +e
/tmp/audit-work/app_path_probe
probe_status=$?
set -e
printf 'unshimmed_probe_exit_code=%s\n' "$probe_status"
test "$probe_status" -ne 0
printf '%s\n' 'COMMAND: LD_PRELOAD=compatibility-shim application-path probe'
LD_PRELOAD=/tmp/audit-work/05_proc_exe_compat.so \
  /tmp/audit-work/app_path_probe
printf '%s\n' 'COMMAND: pinned Lean and Lake versions with compatibility shim'
LD_PRELOAD=/tmp/audit-work/05_proc_exe_compat.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
LD_PRELOAD=/tmp/audit-work/05_proc_exe_compat.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake --version
