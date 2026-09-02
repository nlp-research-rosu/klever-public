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

printf '%s\n' '$ cp reviewer operational specs from evidence to scratch'
cp "$evidence/operational-context.k" "$scratch/operational-context.k"
copy_context_status=$?
cp "$evidence/bridge-body-mutation.k" "$scratch/bridge-body-mutation.k"
copy_mutation_status=$?
printf 'context_copy_exit=%s mutation_copy_exit=%s\n' \
  "$copy_context_status" "$copy_mutation_status"
if (( copy_context_status != 0 || copy_mutation_status != 0 )); then
  exit 1
fi

cd "$scratch" || exit 1
export PATH="$HOME/.nix-profile/bin:$PATH"

run_bounded stage5-inner-context-base \
  kprove operational-context.k \
    --definition audit-verification-base-kompiled \
    --spec-module AUDIT-INNER-CONTEXT-BASE
if (( LAST_STATUS != 0 )) ||
   ! grep -Fxq '#Top' "$evidence/stage5-inner-context-base.log"; then
  failures=$((failures + 1))
fi

run_bounded stage5-inner-context-extended \
  kprove operational-context.k \
    --definition audit-verification-inner-kompiled \
    --spec-module AUDIT-INNER-CONTEXT-EXTENDED
if (( LAST_STATUS != 0 )) ||
   ! grep -Fxq '#Top' "$evidence/stage5-inner-context-extended.log"; then
  failures=$((failures + 1))
fi

run_bounded stage5-outer-context-base \
  kprove operational-context.k \
    --definition audit-verification-inner-kompiled \
    --spec-module AUDIT-OUTER-CONTEXT-BASE
if (( LAST_STATUS != 0 )) ||
   ! grep -Fxq '#Top' "$evidence/stage5-outer-context-base.log"; then
  failures=$((failures + 1))
fi

run_bounded stage5-outer-context-extended \
  kprove operational-context.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-OUTER-CONTEXT-EXTENDED
if (( LAST_STATUS != 0 )) ||
   ! grep -Fxq '#Top' "$evidence/stage5-outer-context-extended.log"; then
  failures=$((failures + 1))
fi

run_bounded stage5-body-mutation-dry-run \
  kprove bridge-body-mutation.k \
    --definition audit-verification-base-kompiled \
    --spec-module AUDIT-BRIDGE-BODY-MUTATION \
    --dry-run
if (( LAST_STATUS != 0 )); then
  failures=$((failures + 1))
fi

run_bounded stage5-body-mutation-proof \
  kprove bridge-body-mutation.k \
    --definition audit-verification-base-kompiled \
    --spec-module AUDIT-BRIDGE-BODY-MUTATION
if (( LAST_STATUS == 0 )); then
  printf '%s\n' 'unexpected_success=1' \
    >> "$evidence/stage5-body-mutation-proof.log"
  failures=$((failures + 1))
fi
if ! grep -q 'WarnStuckClaimState' \
     "$evidence/stage5-body-mutation-proof.log"; then
  printf '%s\n' 'missing_expected_stuck_residual=1' \
    >> "$evidence/stage5-body-mutation-proof.log"
  failures=$((failures + 1))
fi
if ! grep -Eq '"j".*2|2.*"j"' \
     "$evidence/stage5-body-mutation-proof.log"; then
  printf '%s\n' 'missing_expected_j_two_witness=1' \
    >> "$evidence/stage5-body-mutation-proof.log"
  failures=$((failures + 1))
fi

printf 'stage5_dynamic_failures=%s\n' "$failures"
if (( failures != 0 )); then
  printf '%s\n' 'stage5_script_exit=1'
  exit 1
fi
printf '%s\n' 'stage5_script_exit=0'
