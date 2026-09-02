#!/usr/bin/env bash
set -u

SOURCE=/tmp/audit-work/source
BUILD=/tmp/audit-work/build
EVIDENCE=/audit-output/evidence
status=0

run_logged() {
  local label="$1"
  shift
  local log="$EVIDENCE/$label.log"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$log" 2>&1
  local rc=$?
  printf '[exit %d]\n' "$rc" >> "$log"
  printf '[exit %d; log %s]\n' "$rc" "$log"
  tail -100 "$log"
  if (( rc != 0 )); then
    status=1
  fi
}

cd "$SOURCE" || exit 1
printf 'Stage 4: program identity and ground postcondition witnesses\n'

run_logged stage4-kompile-identity \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module VERIFICATION \
    --output-definition "$BUILD/identity-kompiled"

run_logged stage4-parse-solution \
  krun "$SOURCE/solution.mpy" \
    --definition "$BUILD/identity-kompiled" \
    --depth 0 \
    --output json

run_logged stage4-parse-macro \
  krun "$EVIDENCE/program-macro.mpy" \
    --definition "$BUILD/identity-kompiled" \
    --depth 0 \
    --output json

run_logged stage4-compare-expanded-program \
  cmp -s "$EVIDENCE/stage4-parse-solution.log" "$EVIDENCE/stage4-parse-macro.log"

run_logged stage4-ground-python \
  python3 "$EVIDENCE/ground_python_results.py"

run_logged stage4-ground-kprove \
  kprove "$EVIDENCE/ground-spec.k" \
    --definition "$BUILD/verification-kompiled" \
    --spec-module GROUND-SPEC

printf '\nFinal stage4_status=%d\n' "$status"
exit "$status"
