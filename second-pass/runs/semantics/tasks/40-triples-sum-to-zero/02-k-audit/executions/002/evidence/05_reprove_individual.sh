#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
overall=0

cd "$work"
for label in empty length-one length-two length-three length-four length-five length-six; do
  log="$evidence/05_kprove_${label}.log"
  {
    printf 'COMMAND: timeout 900 kprove spec.k --definition verification-kompiled --spec-module SPEC --claims %q --output pretty\n' "$label"
    timeout 900 kprove spec.k \
      --definition verification-kompiled \
      --spec-module SPEC \
      --claims "$label" \
      --output pretty
    status=$?
    printf 'EXIT_STATUS=%s\n' "$status"
  } > "$log" 2>&1
  printf '%s exit=%s\n' "$(basename "$log")" "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
done
exit "$overall"
