#!/usr/bin/env bash
set -euo pipefail

audit_k_dir=/tmp/audit-work/k-operational
cd "$audit_k_dir"

echo '$ kprove operational-spec.k --definition operational-kompiled --spec-module OPERATIONAL-SPEC --output pretty'
kprove operational-spec.k \
  --definition operational-kompiled \
  --spec-module OPERATIONAL-SPEC \
  --output pretty
