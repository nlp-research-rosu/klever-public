gcc -shared -fPIC -O2 -Wall -Wextra -o /tmp/audit-work/liblean_proc_exe_shim.so /audit-output/evidence/lean_proc_exe_shim.c -ldl
LD_PRELOAD=/tmp/audit-work/liblean_proc_exe_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/liblean_proc_exe_shim.so lake --version
