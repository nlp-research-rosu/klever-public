#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/46-fib4
evidence=/audit-output/evidence
summary="$evidence/stage3-reconstruction.log"
: > "$summary"

render_command() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
}

run_logged() {
  local name=$1
  shift
  local logfile="$evidence/$name.log"
  render_command "$@" | tee -a "$summary"
  "$@" 2>&1 | tee "$logfile"
  local rc=${PIPESTATUS[0]}
  printf 'EXIT_STATUS=%s\n' "$rc" | tee -a "$summary" "$logfile"
  return "$rc"
}

run_top() {
  local name=$1
  shift
  if ! run_logged "$name" "$@"; then
    return 1
  fi
  if ! grep -qx '#Top' "$evidence/$name.log"; then
    printf 'TOP_CHECK=FAIL\n' | tee -a "$summary" "$evidence/$name.log"
    return 1
  fi
  printf 'TOP_CHECK=PASS\n' | tee -a "$summary" "$evidence/$name.log"
}

cd "$work" || exit 1
overall=0

run_logged stage3-translate-concrete \
  python3 py2mpy.py concrete_checks.py || overall=1
python3 py2mpy.py concrete_checks.py > concrete_checks.mpy

run_logged stage3-python-concrete python3 concrete_checks.py || overall=1

run_logged stage3-kompile-llvm \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled || overall=1

run_logged stage3-krun-solution \
  krun solution.mpy --definition runtime-fresh-kompiled || overall=1

run_logged stage3-krun-concrete \
  krun concrete_checks.mpy --definition runtime-fresh-kompiled || overall=1

run_logged stage3-kompile-haskell \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-fresh-kompiled || overall=1

run_top stage3-kprove-loop \
  kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant || overall=1

run_top stage3-kprove-complete \
  kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC || overall=1

printf 'OVERALL_EXIT_STATUS=%s\n' "$overall" | tee -a "$summary"
exit "$overall"
