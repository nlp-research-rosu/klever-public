#!/usr/bin/env bash
set -u
set -o pipefail

WORK=/tmp/audit-work/126-is-sorted-audit-003
EVIDENCE=/audit-output/evidence

run_logged() {
  local label=$1
  shift
  local log="$EVIDENCE/$label.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } | tee "$log"
  timeout 300 "$@" 2>&1 | tee -a "$log"
  local command_status=${PIPESTATUS[0]}
  printf 'exit=%s\n' "$command_status" | tee -a "$log"
  return "$command_status"
}

cd "$WORK" || exit 98

entry_build=99
entry_proof=99
body_build=99
body_proof=99

if [[ ! -e audit-no-entry-summary-kompiled ]]; then
  run_logged stage4_no_entry_summary_build \
    kompile verification-no-entry-summary.k \
      --backend haskell \
      --main-module IS-SORTED-WITH-LOOP-LEMMA \
      --syntax-module MPY-SYNTAX \
      --output-definition audit-no-entry-summary-kompiled
  entry_build=$?
else
  printf 'refusing to reuse audit-no-entry-summary-kompiled\n'
  entry_build=97
fi

if [[ "$entry_build" -eq 0 ]]; then
  run_logged stage4_no_entry_summary_proof \
    kprove spec-no-entry-summary.k \
      --definition audit-no-entry-summary-kompiled \
      --spec-module IS-SORTED-SPEC \
      --output pretty
  entry_proof=$?
fi

if [[ ! -e audit-no-body-summary-kompiled ]]; then
  run_logged stage4_no_body_summary_build \
    kompile verification-no-body-summary.k \
      --backend haskell \
      --main-module IS-SORTED-VERIFICATION \
      --syntax-module MPY-SYNTAX \
      --output-definition audit-no-body-summary-kompiled
  body_build=$?
else
  printf 'refusing to reuse audit-no-body-summary-kompiled\n'
  body_build=97
fi

if [[ "$body_build" -eq 0 ]]; then
  run_logged stage4_no_body_summary_proof \
    kprove spec-no-body-summary.k \
      --definition audit-no-body-summary-kompiled \
      --spec-module IS-SORTED-LOOP-SPEC \
      --output pretty
  body_proof=$?
fi

printf 'summary entry_build=%s entry_proof=%s body_build=%s body_proof=%s\n' \
  "$entry_build" "$entry_proof" "$body_build" "$body_proof" \
  | tee "$EVIDENCE/stage4_bridge_dependence_summary.log"

exit 0
