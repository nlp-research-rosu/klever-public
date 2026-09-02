#!/usr/bin/env bash
set -euo pipefail

shim_source=/audit-output/evidence/proc_self_readlink_shim.c
shim_library=/tmp/audit-work/proc_self_readlink_shim.so
lean_root=/opt/elan/toolchains/leanprover--lean4---v4.22.0

nl -ba "${shim_source}"
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o "${shim_library}" "${shim_source}" -ldl
sha256sum "${shim_source}" "${shim_library}"
env \
  LD_PRELOAD="${shim_library}" \
  LEAN_SYSROOT="${lean_root}" \
  "${lean_root}/bin/lean" --version
env \
  LD_PRELOAD="${shim_library}" \
  LEAN_SYSROOT="${lean_root}" \
  "${lean_root}/bin/lake" --version
