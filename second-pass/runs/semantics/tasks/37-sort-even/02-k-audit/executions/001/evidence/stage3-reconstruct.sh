#!/usr/bin/env bash
set -u

work=/tmp/audit-work/37-sort-even-audit/reconstruction-fresh
evidence=/audit-output/evidence
overall=0

run_recorded() {
  name=$1
  shift
  log="$evidence/$name.log"
  (
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    command_status=$?
    echo "exit=$command_status"
    exit "$command_status"
  ) > "$log" 2>&1
  command_status=$?
  echo "$name exit=$command_status"
  overall=$((overall | command_status))
}

echo '$ cd /tmp/audit-work/37-sort-even-audit/reconstruction-fresh'
cd "$work" || exit 1
echo "exit=$?"

if test -e runtime-kompiled || test -e verification-kompiled; then
  echo 'refusing to reuse an existing compiled definition'
  exit 2
fi

run_recorded stage3-kompile-llvm \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

if test -d runtime-kompiled; then
  run_recorded stage3-krun-solution \
    krun solution.mpy \
    --definition runtime-kompiled \
    --output pretty
  run_recorded stage3-krun-tests \
    krun concrete-tests.mpy \
    --definition runtime-kompiled \
    --output pretty
else
  echo 'runtime-kompiled missing; concrete runs skipped'
  overall=1
fi

run_recorded stage3-kompile-haskell \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  -I . \
  --output-definition verification-kompiled

if test -d verification-kompiled; then
  run_recorded stage3-kprove-loop \
    kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.loop-correct \
    --output pretty

  run_recorded stage3-kprove-entry \
    kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.loop-correct,SPEC.sort-even-correct \
    --trusted SPEC.loop-correct \
    --output pretty
else
  echo 'verification-kompiled missing; proof runs skipped'
  overall=1
fi

echo "stage3_exit=$overall"
exit "$overall"
