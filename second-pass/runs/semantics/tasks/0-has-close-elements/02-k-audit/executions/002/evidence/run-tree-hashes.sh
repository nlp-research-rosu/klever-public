#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/01b-tree-hashes.log
exec > >(tee "$LOG") 2>&1

echo '$ python3 /audit-output/evidence/hash_trees.py'
python3 /audit-output/evidence/hash_trees.py
echo "[exit $?]"
echo '$ complete candidate regular-file SHA-256 manifest'
(cd /candidate && find . -type f -print0 | sort -z | xargs -0 sha256sum) \
  > /audit-output/evidence/01-candidate-files.sha256
echo "[exit ${PIPESTATUS[0]}]"
wc -l /audit-output/evidence/01-candidate-files.sha256
sha256sum /audit-output/evidence/01-candidate-files.sha256
echo "[exit $?]"
