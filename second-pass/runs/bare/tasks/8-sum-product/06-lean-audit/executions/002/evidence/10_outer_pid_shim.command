cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/libouterpid.so \
  /audit-output/evidence/10_outer_pid_shim.c
LD_PRELOAD=/tmp/audit-work/libouterpid.so lean --version
LD_PRELOAD=/tmp/audit-work/libouterpid.so lake --version
