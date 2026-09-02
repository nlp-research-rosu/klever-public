#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

cd "$work" || exit 1
python3 "$evidence/split_claims.py" > "$evidence/08-split-claims.log" 2>&1
split_status=$?
printf 'EXIT_STATUS=%s\n' "$split_status" >> "$evidence/08-split-claims.log"
if [[ "$split_status" -ne 0 ]]; then
  exit "$split_status"
fi

overall=0
for number in 1 2 3 4 5 6; do
  log="$evidence/08-kprove-claim-$number.log"
  module="SPEC-CLAIM-$number"
  (
    printf '$ kprove spec-claim-%s.k --definition verification-kompiled --spec-module %s\n' \
      "$number" "$module"
    kprove "spec-claim-$number.k" \
      --definition verification-kompiled \
      --spec-module "$module"
    status=$?
    printf 'KPROVE_EXIT_STATUS=%s\n' "$status"
    exit "$status"
  ) > "$log" 2>&1
  status=$?
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
done
exit "$overall"
