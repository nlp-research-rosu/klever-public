#!/usr/bin/env bash
set -u
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
work=/tmp/audit-work/fresh

python3 /audit-output/evidence/ground-comparison.py
python_rc=$?
echo "GROUND_PYTHON_EXIT=$python_rc"

kprove /audit-output/evidence/spec-ground-entry.k \
  --definition "$work/verification-kompiled" \
  --spec-module HOW-MANY-TIMES-GROUND-ENTRY-AUDIT
kprove_rc=$?
echo "GROUND_KPROVE_EXIT=$kprove_rc"

exit "$((python_rc != 0 || kprove_rc != 0))"
