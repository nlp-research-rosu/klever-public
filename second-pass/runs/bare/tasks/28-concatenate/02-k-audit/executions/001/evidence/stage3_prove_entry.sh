#!/usr/bin/env bash
set -euxo pipefail

kprove /tmp/audit-work/fresh/spec.k \
  --definition /tmp/audit-work/fresh/proof-kompiled \
  --trusted SPEC.concatenate-loop
