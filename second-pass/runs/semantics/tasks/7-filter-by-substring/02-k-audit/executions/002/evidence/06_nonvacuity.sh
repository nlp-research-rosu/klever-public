#!/usr/bin/env bash
set -u

work=/tmp/audit-work/7-filter-by-substring/candidate
out=/audit-output/evidence

run_logged() {
  name=$1
  shift
  log="$out/06_${name}.log"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  (
    cd "$work" || exit 125
    "$@"
  ) >"$log" 2>&1
  status=$?
  printf 'EXIT: %d\n' "$status"
  lines=$(wc -l <"$log")
  printf 'LOG: %s (%d lines)\n' "$log" "$lines"
  sed -n '1,180p' "$log"
  if (( lines > 240 )); then
    printf '[... bounded log: middle omitted ...]\n'
    tail -n 60 "$log"
  fi
  return "$status"
}

run_logged mutation_diff diff -u spec.k spec-vacuity.k
diff_status=$?
if (( diff_status != 1 )); then
  printf 'Unexpected diff status: %d\n' "$diff_status"
  exit 1
fi

run_logged mutation_dry_run kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module FILTER-SPEC-VACUITY \
  --dry-run
dry_status=$?
if (( dry_status != 0 )); then
  exit 1
fi

run_logged mutation_proof kprove spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module FILTER-SPEC-VACUITY \
  --output pretty
proof_status=$?
if (( proof_status == 0 )); then
  printf 'UNEXPECTED: false postcondition proved\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState|implication check|cannot be rewritten further' \
  "$out/06_mutation_proof.log"; then
  printf 'UNEXPECTED: failure lacked expected unmet proof obligation\n'
  exit 1
fi
printf 'SATISFYING_WITNESS: strings=[] substring=\"a\" actual=[] mutated=[\"a\"]\n'
printf 'EXPECTED_NONZERO_PROOF_EXIT: %d\n' "$proof_status"
exit 0
