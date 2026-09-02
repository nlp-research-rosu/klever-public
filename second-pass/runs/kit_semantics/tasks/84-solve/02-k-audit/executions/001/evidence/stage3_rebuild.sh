#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/84-solve
evidence=/audit-output/evidence
raw=/tmp/audit-work/84-solve/raw-logs
mkdir -p "$raw"

run_bounded() {
  local name=$1
  shift
  local raw_log="$raw/$name.raw.log"
  local evidence_log="$evidence/$name.log"
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } > "$evidence_log"
  set +e
  "$@" > "$raw_log" 2>&1
  local status=$?
  set -e
  {
    printf 'EXIT_STATUS=%s\n' "$status"
    printf 'OUTPUT_LINES=%s\n' "$(wc -l < "$raw_log")"
    sed -n '1,100p' "$raw_log"
    if [[ $(wc -l < "$raw_log") -gt 200 ]]; then
      printf '[... bounded log: middle omitted ...]\n'
      tail -n 100 "$raw_log"
    else
      sed -n '101,200p' "$raw_log"
    fi
  } >> "$evidence_log"
  return "$status"
}

cd "$work"
run_bounded toolchain-kompile-version kompile --version
run_bounded toolchain-kprove-version kprove --version
run_bounded toolchain-krun-version krun --version

sed '$a\
assert solve(0) == "0"\
assert solve(7) == "111"\
assert solve(8) == "1000"\
assert solve(69) == "1111"\
assert solve(79) == "10000"\
assert solve(599) == "10111"\
assert solve(699) == "11000"\
assert solve(4999) == "11111"\
assert solve(5999) == "100000"\
assert solve(9999) == "100100"\
assert solve(10000) == "1"\
assert solve(1000) == "1"\
assert solve(150) == "110"\
assert solve(147) == "1100"' solution.py \
  | python3 py2mpy.py /dev/stdin > concrete-test.mpy
cp concrete-test.mpy "$evidence/concrete-test.mpy"

run_bounded stage3-kompile-llvm \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-audit-kompiled

run_bounded stage3-krun-concrete \
  krun concrete-test.mpy --definition runtime-audit-kompiled

run_bounded stage3-kompile-bridge-haskell \
  kompile bridge-verification.k \
    --backend haskell \
    --main-module BRIDGE-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition bridge-audit-kompiled

run_bounded stage3-kompile-proof-haskell \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-audit-kompiled
