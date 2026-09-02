#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/0-has-close-elements
evidence=/audit-output/evidence
build="$scratch/audit-build"
mkdir -p "$build"

run_logged() {
  log_name=$1
  shift
  log="$evidence/$log_name"
  {
    printf 'WORKDIR: %s\n' "$scratch"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  (
    cd "$scratch" || exit 125
    "$@"
  ) >> "$log" 2>&1
  status=$?
  printf 'EXIT: %s\n' "$status" >> "$log"
  printf '%s exit=%s\n' "$log_name" "$status"
  return "$status"
}

overall=0

run_logged 03a-translate-concrete.log \
  python3 py2mpy.py /audit-output/evidence/concrete_semantics_test.py || overall=1
mv "$evidence/03a-translate-concrete.log" "$evidence/03a-translate-concrete.stdout"

# The translator's stdout is the concrete K program. Re-run with a normal output
# artifact so command evidence remains distinct from generated program text.
(
  cd "$scratch" || exit 125
  python3 py2mpy.py /audit-output/evidence/concrete_semantics_test.py > reviewer-concrete.mpy
)
status=$?
{
  printf 'WORKDIR: %s\n' "$scratch"
  printf '%s\n' 'COMMAND: python3 py2mpy.py /audit-output/evidence/concrete_semantics_test.py > reviewer-concrete.mpy'
  printf 'EXIT: %s\n' "$status"
  sha256sum "$scratch/reviewer-concrete.mpy"
} > "$evidence/03a-translate-concrete.log"
if [[ $status -ne 0 ]]; then overall=1; fi

run_logged 03b-kompile-llvm.log \
  kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition "$build/runtime-kompiled" || overall=1

run_logged 03c-python-concrete.log \
  python3 /audit-output/evidence/concrete_semantics_test.py || overall=1

run_logged 03d-krun-concrete.log \
  krun reviewer-concrete.mpy --definition "$build/runtime-kompiled" \
  --output none || overall=1

run_logged 04a-kompile-base.log \
  kompile verification.k --backend haskell \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition "$build/base-kompiled" || overall=1

run_logged 04b-kprove-inner.log \
  kprove spec.k --definition "$build/base-kompiled" \
  --spec-module SPEC-INNER || overall=1

run_logged 04c-kompile-inner.log \
  kompile verification.k --backend haskell \
  --main-module VERIFICATION-WITH-INNER --syntax-module MPY-SYNTAX \
  --output-definition "$build/inner-kompiled" || overall=1

run_logged 04d-kprove-helper.log \
  kprove spec.k --definition "$build/inner-kompiled" \
  --spec-module SPEC-HELPER || overall=1

run_logged 04e-kompile-helper.log \
  kompile verification.k --backend haskell \
  --main-module VERIFICATION-WITH-HELPER --syntax-module MPY-SYNTAX \
  --output-definition "$build/helper-kompiled" || overall=1

run_logged 04f-kprove-outer.log \
  kprove spec.k --definition "$build/helper-kompiled" \
  --spec-module SPEC-OUTER || overall=1

run_logged 04g-kompile-outer.log \
  kompile verification.k --backend haskell \
  --main-module VERIFICATION-WITH-OUTER --syntax-module MPY-SYNTAX \
  --output-definition "$build/outer-kompiled" || overall=1

run_logged 04h-kprove-entry.log \
  kprove spec.k --definition "$build/outer-kompiled" \
  --spec-module SPEC-ENTRY || overall=1

run_logged 04i-kompile-entry.log \
  kompile verification.k --backend haskell \
  --main-module VERIFICATION-WITH-ENTRY --syntax-module MPY-SYNTAX \
  --output-definition "$build/entry-kompiled" || overall=1

run_logged 04j-kprove-final.log \
  kprove spec.k --definition "$build/entry-kompiled" \
  --spec-module SPEC || overall=1

printf 'overall_exit=%s\n' "$overall"
exit "$overall"
