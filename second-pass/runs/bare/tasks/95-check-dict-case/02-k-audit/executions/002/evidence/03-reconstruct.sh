#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/95-check-dict-case-audit
status=0

record() {
  label="$1"
  shift
  printf 'COMMAND[%s]:' "$label"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT[%s]=%s\n' "$label" "$command_status"
  if [[ "$command_status" -ne 0 ]]; then
    status=1
  fi
}

printf '%s\n' 'SCRATCH PRE-BUILD CACHE CHECK'
find "$scratch" -maxdepth 1 -name '*-kompiled' -print
cache_status=0
if find "$scratch" -maxdepth 1 -name '*-kompiled' -print -quit | grep -q .; then
  cache_status=1
  status=1
fi
printf 'PREEXISTING_CACHE_EXIT=%s\n' "$cache_status"

record "kompile-version" kompile --version
record "kprove-version" kprove --version
record "krun-version" krun --version

(
  cd "$scratch" || exit 1
  record "concrete-kompile" \
    kompile semantic.k \
      --main-module MPY \
      --syntax-module MPY-SYNTAX \
      --backend llvm \
      --output-definition concrete-fresh-kompiled
  record "proof-kompile" \
    kompile verification.k \
      --main-module VERIFICATION \
      --syntax-module VERIFICATION \
      --backend haskell \
      --output-definition verification-fresh-kompiled
  record "all-unmodified-claims" \
    kprove spec.k \
      --definition verification-fresh-kompiled \
      --spec-module SPEC

  cp /audit-output/evidence/spec-labeled.k spec-labeled.k
  labels=(
    case-01-empty
    case-02-lower
    case-03-mixed
    case-04-int
    case-05-title
    case-06-upper
    case-07-lower-uncased
    case-08-upper-uncased
    case-09-uncased
    case-10-single-mixed
    case-11-bool
  )
  for label in "${labels[@]}"; do
    record "$label" \
      kprove spec-labeled.k \
        --definition verification-fresh-kompiled \
        --spec-module SPEC-LABELED \
        --claims "SPEC-LABELED.$label"
  done
  exit "$status"
)
subshell_status=$?
if [[ "$subshell_status" -ne 0 ]]; then
  status=1
fi

printf 'RECONSTRUCTION_STATUS=%s\n' "$status"
exit "$status"
