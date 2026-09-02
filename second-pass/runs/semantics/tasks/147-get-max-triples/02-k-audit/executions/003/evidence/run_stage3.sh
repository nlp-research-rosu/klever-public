#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/147-get-max-triples-clean || exit 1
status=0

record() {
  log=$1
  shift
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1 | tee "/audit-output/evidence/$log"
  rc=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
  return "$rc"
}

record versions.log kompile --version
record python-version.log python3 --version

printf '$ test no preexisting compiled definitions\n'
if find . -maxdepth 1 -type d -name '*-kompiled' -print | grep -q .; then
  find . -maxdepth 1 -type d -name '*-kompiled' -print
  printf '[exit 1]\n'
  exit 1
fi
printf '[exit 0; none found]\n'

record kompile-llvm.log \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
if (( status != 0 )); then
  printf 'FINAL_STATUS=%d\n' "$status"
  exit "$status"
fi

record krun-concrete.log \
  krun concrete_tests.mpy \
  --definition runtime-audit-kompiled \
  --output pretty

record kompile-haskell.log \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled \
  -I .
if (( status != 0 )); then
  printf 'FINAL_STATUS=%d\n' "$status"
  exit "$status"
fi

for label in residue-0 residue-1 residue-2 get-max-triples-correct; do
  record "kprove-$label.log" \
    kprove spec.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC \
    --claims "SPEC.$label" \
    -I . \
    --output pretty
  if ! grep -Fxq '#Top' "/audit-output/evidence/kprove-$label.log"; then
    printf '[missing exact #Top for %s]\n' "$label"
    status=1
  fi
done

printf 'FINAL_STATUS=%d\n' "$status"
exit "$status"
