#!/usr/bin/env bash
set +e

echo '$ cmp candidate source artifacts with scratch build source artifacts'
for name in semantic.k verification.k spec.k solution.mpy
do
  cmp -s "/candidate/$name" "/tmp/audit-work/build/$name"
  echo "$name exit=$?"
done

echo '$ sha256sum candidate and scratch build source artifacts'
sha256sum \
  /candidate/semantic.k /tmp/audit-work/build/semantic.k \
  /candidate/verification.k /tmp/audit-work/build/verification.k \
  /candidate/spec.k /tmp/audit-work/build/spec.k \
  /candidate/solution.mpy /tmp/audit-work/build/solution.mpy
echo "exit=$?"
