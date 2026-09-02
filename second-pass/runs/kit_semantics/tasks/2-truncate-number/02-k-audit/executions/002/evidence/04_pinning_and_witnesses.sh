#!/usr/bin/env bash
set -euo pipefail
set -x

python3 /audit-output/evidence/04_constructor_pinning.py

cd /tmp/audit-work/fresh
kprove spec-witnesses.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-WITNESSES

