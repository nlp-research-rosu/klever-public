#!/usr/bin/env bash
set -uo pipefail

workdir=/tmp/audit-work/reconstruction
evidence_dir=/audit-output/evidence
labels=(
  bad-dot-count
  bad-initial
  bad-extension
  too-many-digits-txt
  too-many-digits-exe
  too-many-digits-dll
  valid-name-txt
  valid-name-exe
  valid-name-dll
)

overall=0
pids=()
pid_labels=()

wait_batch() {
  local index
  local status
  for index in "${!pids[@]}"; do
    if wait "${pids[$index]}"; then
      status=0
    else
      status=$?
      overall=1
    fi
    printf 'claim=%s exit=%s\n' "${pid_labels[$index]}" "$status"
  done
  pids=()
  pid_labels=()
}

for label in "${labels[@]}"; do
  (
    cd "$workdir" || exit 125
    script -q -e -c \
      "kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC --claims SPEC.$label" \
      "$evidence_dir/03-kprove-$label.log"
  ) &
  pids+=("$!")
  pid_labels+=("$label")
  if [[ ${#pids[@]} -eq 3 ]]; then
    wait_batch
  fi
done

if [[ ${#pids[@]} -ne 0 ]]; then
  wait_batch
fi

exit "$overall"
