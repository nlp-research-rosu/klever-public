#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words

echo '$ python3 /audit-output/evidence/04_generate_pinning.py'
python3 /audit-output/evidence/04_generate_pinning.py
echo "generate_pinning_exit=$?"

echo '$ kprove audit-pinning.k --definition audit-verification-kompiled --spec-module PINNING-SPEC'
kprove audit-pinning.k \
  --definition audit-verification-kompiled \
  --spec-module PINNING-SPEC
echo "pinning_kprove_exit=$?"

echo '$ sha256sum solution.mpy regenerated-solution.mpy audit-pinning.k'
sha256sum solution.mpy regenerated-solution.mpy audit-pinning.k
echo "pinning_hash_exit=$?"
