#!/usr/bin/env bash
set -euo pipefail
set -x

export PATH=/home/agent/.nix-profile/bin:$PATH
cd /tmp/audit-work/case

claim_label="$1"
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims "$claim_label" \
  --output pretty
