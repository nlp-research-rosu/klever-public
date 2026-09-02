#!/usr/bin/env bash
set -euo pipefail
set -x

export PATH=/home/agent/.nix-profile/bin:$PATH
cd /tmp/audit-work/case

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --output pretty
