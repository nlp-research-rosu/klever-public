#!/usr/bin/env bash
set -euo pipefail

audit_work=/tmp/audit-work/25-factorize
if [[ -e "$audit_work" ]]; then
  echo "Refusing to overwrite existing scratch path: $audit_work" >&2
  exit 2
fi

mkdir -p "$audit_work"
cp /candidate/solution.py "$audit_work/solution.py"
cp /candidate/solution.mpy "$audit_work/solution.mpy.submitted"
cp /candidate/spec.k "$audit_work/spec.k"
cp /candidate/verification.k "$audit_work/verification.k"
cp /candidate/prove.sh "$audit_work/prove.sh.candidate"
cp /candidate/concrete_tests.py "$audit_work/concrete_tests.py.candidate"
cp /candidate/concrete-tests.mpy "$audit_work/concrete-tests.mpy.candidate"
cp /reference/canonical.py "$audit_work/canonical.py"
cp /reference/prompt.py "$audit_work/prompt.py"
cp /reference/py2mpy.py "$audit_work/py2mpy.py"
cp -R /reference/reference-semantics "$audit_work/reference-semantics"

find "$audit_work" -type f -printf '%P\n' | sort
