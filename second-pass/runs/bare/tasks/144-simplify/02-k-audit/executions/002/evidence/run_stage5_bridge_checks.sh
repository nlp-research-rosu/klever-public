#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction

for label in slash-split-connection decimal-value-connection string-int-inverse
do
  set +e
  output="$(kprove bridge-check.k \
    --definition audit-semantic-kompiled \
    --spec-module BRIDGE-CHECK \
    --claims "BRIDGE-CHECK.${label}" 2>&1)"
  status=$?
  set -e
  printf '%s\n' "$output"
  printf 'bridge_free_%s_exit=%s\n' "$label" "$status"
done
