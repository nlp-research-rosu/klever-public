#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/0-has-close-elements
evidence=/audit-output/evidence
failures=0
LAST_STATUS=0

run_bounded() {
  local label=$1
  shift
  local raw="$scratch/${label}.raw.log"
  local log="$evidence/${label}.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  "$@" > "$raw" 2>&1
  LAST_STATUS=$?
  local lines bytes
  lines=$(wc -l < "$raw")
  bytes=$(wc -c < "$raw")
  {
    printf 'exit_status=%s\n' "$LAST_STATUS"
    printf 'raw_output_lines=%s raw_output_bytes=%s\n' "$lines" "$bytes"
    if (( lines <= 320 )); then
      cat "$raw"
    else
      head -n 140 "$raw"
      printf '%s\n' '--- middle omitted from bounded reviewer log ---'
      tail -n 160 "$raw"
    fi
  } >> "$log"
  rm -f "$raw"
  printf '%s exit=%s lines=%s bytes=%s\n' \
    "$label" "$LAST_STATUS" "$lines" "$bytes"
  return 0
}

printf '%s\n' '$ cp reviewer false-result mutation from evidence to scratch'
cp "$evidence/nonvacuity-mutation.k" "$scratch/nonvacuity-mutation.k"
copy_status=$?
printf 'mutation_copy_exit=%s\n' "$copy_status"
if (( copy_status != 0 )); then
  exit 1
fi

cd "$scratch" || exit 1
export PATH="$HOME/.nix-profile/bin:$PATH"

run_bounded stage6-mutation-dry-run \
  kprove nonvacuity-mutation.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-NONVACUITY \
    --dry-run
if (( LAST_STATUS != 0 )); then
  failures=$((failures + 1))
fi

run_bounded stage6-mutation-proof \
  kprove nonvacuity-mutation.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-NONVACUITY
if (( LAST_STATUS == 0 )); then
  printf '%s\n' 'unexpected_success=1' \
    >> "$evidence/stage6-mutation-proof.log"
  failures=$((failures + 1))
fi
if ! grep -q 'WarnStuckClaimState' "$evidence/stage6-mutation-proof.log"; then
  printf '%s\n' 'missing_expected_stuck_residual=1' \
    >> "$evidence/stage6-mutation-proof.log"
  failures=$((failures + 1))
fi
if ! grep -A3 '<k>' "$evidence/stage6-mutation-proof.log" |
     grep -q 'false'; then
  printf '%s\n' 'missing_expected_false_result=1' \
    >> "$evidence/stage6-mutation-proof.log"
  failures=$((failures + 1))
fi

printf 'stage6_failures=%s\n' "$failures"
if (( failures != 0 )); then
  printf '%s\n' 'stage6_script_exit=1'
  exit 1
fi
printf '%s\n' 'stage6_script_exit=0'
