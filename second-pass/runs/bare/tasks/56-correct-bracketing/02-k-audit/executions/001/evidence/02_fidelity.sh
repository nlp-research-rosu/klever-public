#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
regenerated="$scratch/solution.regenerated.mpy"

echo 'AUDITOR COMMAND: python3 trusted py2mpy.py candidate solution.py > scratch/solution.regenerated.mpy'
python3 "$scratch/reference/py2mpy.py" \
  "$scratch/candidate-src/solution.py" > "$regenerated"
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: cmp -s regenerated MPY submitted MPY'
cmp -s "$regenerated" "$scratch/candidate-src/solution.mpy"
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: sha256sum regenerated MPY submitted MPY'
sha256sum "$regenerated" "$scratch/candidate-src/solution.mpy"
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: diff -u trusted canonical.py candidate solution.py'
diff -u "$scratch/reference/canonical.py" "$scratch/candidate-src/solution.py"
status=$?
echo "EXIT STATUS: $status (1 means source text differs; behavior is tested separately)"

echo 'AUDITOR COMMAND: python3 independent differential script'
python3 /audit-output/evidence/02_differential.py
status=$?
echo "EXIT STATUS: $status"
exit "$status"
