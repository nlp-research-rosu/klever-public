#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words

echo '$ python3 /audit-output/evidence/09_claim_witnesses.py'
python3 /audit-output/evidence/09_claim_witnesses.py
echo "claim_witnesses_exit=$?"

echo '$ python3 /audit-output/evidence/09_make_ground_program.py'
python3 /audit-output/evidence/09_make_ground_program.py
echo "make_ground_program_exit=$?"

echo '$ python3 py2mpy.py audit-ground-witnesses.py > audit-ground-witnesses.mpy'
python3 py2mpy.py audit-ground-witnesses.py > audit-ground-witnesses.mpy
echo "ground_translation_exit=$?"

echo '$ krun audit-ground-witnesses.mpy --definition audit-runtime-kompiled'
krun audit-ground-witnesses.mpy --definition audit-runtime-kompiled
echo "ground_krun_exit=$?"

cp /audit-output/evidence/09_semantic_boundary.k semantic-boundary.k
echo '$ kprove semantic-boundary.k --definition audit-fixed-kompiled --spec-module SEMANTIC-BOUNDARY --claims SEMANTIC-BOUNDARY.modeled-result'
kprove semantic-boundary.k \
  --definition audit-fixed-kompiled \
  --spec-module SEMANTIC-BOUNDARY \
  --claims SEMANTIC-BOUNDARY.modeled-result
echo "modeled_boundary_kprove_exit=$?"

echo '$ kprove semantic-boundary.k --definition audit-fixed-kompiled --spec-module SEMANTIC-BOUNDARY --claims SEMANTIC-BOUNDARY.cpython-result'
kprove semantic-boundary.k \
  --definition audit-fixed-kompiled \
  --spec-module SEMANTIC-BOUNDARY \
  --claims SEMANTIC-BOUNDARY.cpython-result
echo "cpython_boundary_kprove_exit=$?"
