#!/usr/bin/env bash
set -u

echo 'COMMAND: python3 /audit-output/evidence/01_provenance.py'
python3 /audit-output/evidence/01_provenance.py
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: cmp -s /candidate/prompt.py /reference/prompt.py'
cmp -s /candidate/prompt.py /reference/prompt.py
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: cmp -s /candidate/py2mpy.py /reference/py2mpy.py'
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: compare sorted entry-type manifests for supplied semantics'
reference_manifest=/tmp/audit-work/reference-semantics-types.txt
candidate_manifest=/tmp/audit-work/candidate-semantics-types.txt
find /reference/reference-semantics -printf '%y %P -> %l\n' | LC_ALL=C sort > "$reference_manifest"
find /candidate/reference-semantics -printf '%y %P -> %l\n' | LC_ALL=C sort > "$candidate_manifest"
cmp -s "$reference_manifest" "$candidate_manifest"
status=$?
echo "EXIT_STATUS: $status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

echo 'COMMAND: sha256sum every regular mounted candidate file (sorted path order)'
find /candidate -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
status=$?
echo "EXIT_STATUS: $status"
exit "$status"
