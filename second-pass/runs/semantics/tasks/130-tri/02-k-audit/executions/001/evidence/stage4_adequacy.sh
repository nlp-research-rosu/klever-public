#!/usr/bin/env bash
set -u
set -o pipefail

work_dir=/tmp/audit-work/reconstruction
cd "$work_dir" || exit 90

echo '$ python3 /audit-output/evidence/stage4_witness.py'
python3 /audit-output/evidence/stage4_witness.py
witness_rc=$?
echo "exit=$witness_rc"

echo '$ cp /audit-output/evidence/spec-exact-strengthening.k /tmp/audit-work/reconstruction/spec-exact-strengthening.k'
cp /audit-output/evidence/spec-exact-strengthening.k \
  /tmp/audit-work/reconstruction/spec-exact-strengthening.k
copy_rc=$?
echo "exit=$copy_rc"

echo '$ kprove spec-exact-strengthening.k --definition verification-kompiled --spec-module TRI-EXACT-STRENGTHENING-SPEC --output pretty'
kprove spec-exact-strengthening.k \
  --definition verification-kompiled \
  --spec-module TRI-EXACT-STRENGTHENING-SPEC \
  --output pretty
exact_rc=$?
echo "exit=$exact_rc"
echo "SUMMARY witness=$witness_rc copy=$copy_rc exact_strengthening=$exact_rc"

# A nonzero exact-strengthening proof is an expected adequacy finding, not a
# script execution failure. The log preserves its actual status and residual.
if [ "$witness_rc" -ne 0 ] || [ "$copy_rc" -ne 0 ]; then
  exit 1
fi
exit 0
