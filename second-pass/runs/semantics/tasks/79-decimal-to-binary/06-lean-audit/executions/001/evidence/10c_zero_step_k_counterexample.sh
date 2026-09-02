#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/k-operational

echo '$ kprove operational-spec.k --definition operational-kompiled --spec-module OPERATIONAL-SPEC --output pretty'
kprove operational-spec.k \
  --definition operational-kompiled \
  --spec-module OPERATIONAL-SPEC \
  --output pretty
