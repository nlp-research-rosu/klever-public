#!/usr/bin/env bash
set -uo pipefail

echo '$ PYTHONPATH=/reference python3 /audit-output/evidence/03_hash_and_lemma_identity.py'
PYTHONPATH=/reference python3 /audit-output/evidence/03_hash_and_lemma_identity.py

echo '$ command -v kompile; kompile --version'
command -v kompile
kompile --version

echo '$ command -v kprove; kprove --version'
command -v kprove
kprove --version

echo '$ command -v lake; lake --version'
command -v lake
lake --version
