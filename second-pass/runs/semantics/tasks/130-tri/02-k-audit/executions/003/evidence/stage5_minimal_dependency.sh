#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/130-tri-audit
evidence=/audit-output/evidence
minimal="$scratch/verification-minimal.k"
minimal_spec="$scratch/spec-minimal.k"
definition="$scratch/verification-minimal-kompiled"
overall=0

printf 'COMMAND: remove verification.k lines 44, 48-49, 52, and 59-62 (all triPrefix declarations/rules)\n'
sed -e '44d' -e '48,49d' -e '52d' -e '59,62d' "$scratch/verification.k" > "$minimal"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi
cp "$minimal" "$evidence/verification_minimal.k"

printf '\nCOMMAND: point a copied spec at verification-minimal.k\n'
sed '1c requires "/tmp/audit-work/130-tri-audit/verification-minimal.k"' \
  "$scratch/spec.k" > "$minimal_spec"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi
cp "$minimal_spec" "$evidence/spec_minimal.k"

run_logged() {
  name=$1
  shift
  log="$evidence/$name.full.log"
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\nFULL_LOG: %s\n' "$log"
  "$@" >"$log" 2>&1
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  sed -n '1,180p' "$log"
  if [[ "$status" -ne 0 ]]; then overall=1; fi
}

run_logged stage5_minimal_build \
  kompile "$minimal" \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition"

run_logged stage5_minimal_loop \
  kprove "$minimal_spec" \
  --definition "$definition" \
  --spec-module TRI-LOOP-SPEC \
  --output pretty

run_logged stage5_minimal_entry \
  kprove "$minimal_spec" \
  --definition "$definition" \
  --spec-module TRI-CORRECT-SPEC \
  --output pretty

for log in "$evidence/stage5_minimal_loop.full.log" "$evidence/stage5_minimal_entry.full.log"; do
  count=$(grep -c '^#Top$' "$log" || true)
  printf 'TOP_COUNT file=%s count=%s\n' "$log" "$count"
  if [[ "$count" -ne 1 ]]; then overall=1; fi
done

printf '\nSTAGE5_MINIMAL_DEPENDENCY_EXIT_STATUS: %d\n' "$overall"
exit "$overall"
