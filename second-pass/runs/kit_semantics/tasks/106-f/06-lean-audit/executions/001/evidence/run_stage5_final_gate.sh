#!/usr/bin/env bash
set -u

toolchain=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export PYTHONPATH=/reference
export LD_PRELOAD=/tmp/audit-work/lean_proc_compat.so
export PATH="$toolchain/bin:$PATH"
export LEAN="$toolchain/bin/lean"
export LEAN_SYSROOT="$toolchain/"
export LAKE_HOME="$toolchain/"
export LAKE_OVERRIDE_LEAN=1

python3 /audit-output/evidence/run_stage5_final_gate.py
status=$?
echo "trusted_stage5_final_gate_exit=$status"
exit "$status"
