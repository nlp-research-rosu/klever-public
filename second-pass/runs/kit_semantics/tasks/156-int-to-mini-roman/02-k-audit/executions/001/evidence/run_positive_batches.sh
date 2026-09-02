#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/rebuild || exit 1

for batch_number in $(seq 0 9); do
  first=$((batch_number * 100 + 1))
  last=$((first + 99))
  batch=$(printf '%02d' $((batch_number + 1)))
  labels=""
  for number in $(seq "$first" "$last"); do
    label=$(printf 'SPEC.roman-%04d' "$number")
    if [ -z "$labels" ]; then
      labels=$label
    else
      labels="${labels},${label}"
    fi
  done

  batch_log="/audit-output/evidence/kprove_positive_${batch}.log"
  started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  printf 'BATCH_START batch=%s range=%s..%s utc=%s\n' \
    "$batch" "$first" "$last" "$started"

  bash /audit-output/evidence/run_capture.sh "$batch_log" \
    kprove spec.k \
      --definition verification-kompiled \
      --spec-module SPEC \
      --claims "$labels"
  batch_rc=$?
  top_count=$(rg -c '^#Top$' "$batch_log" || true)
  ended=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  printf 'BATCH_END batch=%s range=%s..%s rc=%s top_count=%s utc=%s\n' \
    "$batch" "$first" "$last" "$batch_rc" "$top_count" "$ended"

  if [ "$batch_rc" -ne 0 ] || [ "$top_count" -ne 1 ]; then
    exit 1
  fi
done

printf 'ALL_POSITIVE_BATCHES=PASS claims=1000 range=1..1000\n'
