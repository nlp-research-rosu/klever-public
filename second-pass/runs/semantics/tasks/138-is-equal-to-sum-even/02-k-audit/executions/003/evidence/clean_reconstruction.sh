#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
overall=0

run_logged() {
  local label=$1
  shift
  local log="$evidence/$label.log"
  {
    printf 'CWD: %s\n' "$work"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  (
    cd "$work" || exit 99
    "$@"
  ) >> "$log" 2>&1
  local status=$?
  printf 'EXIT_STATUS: %s\n' "$status" >> "$log"
  printf '%-30s exit=%s log=%s\n' "$label" "$status" "$log"
  if (( status != 0 )); then
    overall=1
  fi
  return 0
}

cp "$evidence/concrete_audit.py" "$work/concrete-audit.py"
cp "$evidence"/spec-claim-?.k "$work/"

run_logged translate-concrete \
  python3 py2mpy.py concrete-audit.py
(
  cd "$work" || exit 99
  python3 py2mpy.py concrete-audit.py > concrete-audit.mpy
)
translate_write_status=$?
printf 'translate-write                exit=%s\n' "$translate_write_status"
if (( translate_write_status != 0 )); then
  overall=1
fi

run_logged kompile-runtime \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-audit-kompiled

run_logged krun-concrete \
  krun concrete-audit.mpy \
    --definition runtime-audit-kompiled

run_logged kompile-verification \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module VERIFICATION \
    --output-definition verification-audit-kompiled

run_logged kprove-original-spec \
  kprove spec.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC

for claim in 1 2 3 4; do
  run_logged "kprove-claim-$claim" \
    kprove "spec-claim-$claim.k" \
      --definition verification-audit-kompiled \
      --spec-module "SPEC-CLAIM-$claim"
done

printf 'OVERALL_EXIT_STATUS: %s\n' "$overall"
exit "$overall"
