#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/19-sort-numbers/source
definition=/tmp/audit-work/19-sort-numbers/verification-kompiled
evidence=/audit-output/evidence
claims=(zero one two three four five six seven eight nine)
overall=0

cd "$source_dir" || exit 2
for word in "${claims[@]}"; do
  logfile="$evidence/stage3-proof-key-$word.log"
  command="/audit-output/evidence/scripts/run_logged.sh kprove spec.k --definition $definition --spec-module SPEC --claims SPEC.key-$word"
  printf 'LOG_COMMAND: script -q -e -c %q %q\n' "$command" "$logfile"
  script -q -e -c "$command" "$logfile"
  status=$?
  top_count=$(grep -c '#Top' "$logfile")
  printf 'CLAIM: SPEC.key-%s EXIT_STATUS: %d TOP_COUNT: %d\n' "$word" "$status" "$top_count"
  if [[ $status -ne 0 || $top_count -lt 1 ]]; then
    overall=1
  fi
done

printf 'ALL_KEY_CLAIMS_OK: %s\n' "$(( overall == 0 ))"
exit "$overall"
