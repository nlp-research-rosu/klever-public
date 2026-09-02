cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/hostpid_shim.so \
  /tmp/audit-work/hostpid_shim.c
LD_PRELOAD=/tmp/audit-work/hostpid_shim.so lean --version
