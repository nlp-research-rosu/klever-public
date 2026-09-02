#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/37-sort-even-audit
source_dir=$scratch/source
trusted_dir=$scratch/trusted
evidence=/audit-output/evidence
status=0

echo '$ cd /tmp/audit-work/37-sort-even-audit/source'
cd "$source_dir" || exit 1
echo "exit=$?"

echo '$ python3 ../trusted/py2mpy.py solution.py > ../regenerated-solution.mpy'
python3 "$trusted_dir/py2mpy.py" solution.py > "$scratch/regenerated-solution.mpy"
translator_status=$?
echo "exit=$translator_status"
status=$((status | translator_status))

echo '$ cmp -s solution.mpy ../regenerated-solution.mpy'
cmp -s solution.mpy "$scratch/regenerated-solution.mpy"
cmp_status=$?
echo "exit=$cmp_status"
status=$((status | cmp_status))

echo '$ sha256sum solution.mpy ../regenerated-solution.mpy'
sha256sum solution.mpy "$scratch/regenerated-solution.mpy"
hash_status=$?
echo "exit=$hash_status"
status=$((status | hash_status))

echo '$ python3 /audit-output/evidence/differential_test.py ../trusted/canonical.py solution.py /audit-output/evidence/differential-inputs.json'
python3 "$evidence/differential_test.py" \
  "$trusted_dir/canonical.py" \
  "$source_dir/solution.py" \
  "$evidence/differential-inputs.json"
differential_status=$?
echo "exit=$differential_status"
status=$((status | differential_status))

echo "stage2_exit=$status"
exit "$status"
