#!/usr/bin/env bash
set -euo pipefail

work_dir=/tmp/audit-work/reconstruction

python3 /audit-output/evidence/make_concrete_program.py
python3 "$work_dir/py2mpy.py" "$work_dir/concrete_audit.py" \
  > "$work_dir/concrete_audit.mpy"
kompile "$work_dir/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work_dir/concrete-kompiled"
krun "$work_dir/concrete_audit.mpy" \
  --definition "$work_dir/concrete-kompiled"
