#!/usr/bin/env bash
set -u

work=/tmp/audit-work/7-filter-by-substring/bodymutation
out=/audit-output/evidence

run_logged() {
  name=$1
  shift
  log="$out/05_${name}.log"
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

run_logged body_mutation_diff diff -u /candidate/verification.k verification.k
diff_status=$?
if (( diff_status != 1 )); then
  printf 'Unexpected diff status: %d\n' "$diff_status"
  exit 1
fi

run_logged body_mutation_build kompile verification.k \
  --backend haskell \
  --main-module FILTER-VERIFICATION \
  --syntax-module FILTER-VERIFICATION \
  --output-definition body-mutation-kompiled
build_status=$?
if (( build_status != 0 )); then
  exit 1
fi

run_logged body_mutation_proof kprove spec.k \
  --definition body-mutation-kompiled \
  --spec-module FILTER-SPEC \
  --output pretty
proof_status=$?
if (( proof_status == 0 )); then
  printf 'UNEXPECTED: changed body still proved\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState|cannot be rewritten further|implication check' \
  "$out/05_body_mutation_proof.log"; then
  printf 'UNEXPECTED: failure lacked proof residual\n'
  exit 1
fi
printf 'EXPECTED_NONZERO_PROOF_EXIT: %d\n' "$proof_status"
exit 0
