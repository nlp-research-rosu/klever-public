#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 90

echo '$ kprove spec-ground-witness.k --definition verification-kompiled --spec-module HOW-MANY-TIMES-GROUND-WITNESS'
kprove spec-ground-witness.k \
  --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-GROUND-WITNESS
proof_status=$?
echo "exit_status=$proof_status"

echo '$ python3 -c "..."  # trusted canonical and generated Python on the same two witnesses'
python3 -c 'import canonical,solution; cases=[("", "", 1), ("aaaa", "aa", 3)]; print([(s,p,canonical.how_many_times(s,p),solution.how_many_times(s,p),e) for s,p,e in cases]); assert all(canonical.how_many_times(s,p)==e and solution.how_many_times(s,p)==e for s,p,e in cases)'
python_status=$?
echo "exit_status=$python_status"

if (( proof_status || python_status )); then
  exit 1
fi
