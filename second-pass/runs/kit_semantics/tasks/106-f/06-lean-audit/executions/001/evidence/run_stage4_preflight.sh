#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

export PYTHONPATH=/reference
# The audit sandbox exposes a PID namespace without matching /proc/<pid>.
# Lean 4.22 resolves its own executable through that path, so preload the
# minimal compatibility shim that maps only /proc/<digits>/exe to
# /proc/self/exe. The shim source and diagnostic trace are preserved.
export LD_PRELOAD=/tmp/audit-work/lean_proc_compat.so
export PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:"$PATH"
export LEAN=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean
export LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LAKE_OVERRIDE_LEAN=1
python3 /audit-output/evidence/run_stage4_preflight.py
