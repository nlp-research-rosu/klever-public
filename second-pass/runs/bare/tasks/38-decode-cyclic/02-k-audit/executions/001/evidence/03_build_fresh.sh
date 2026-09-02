#!/usr/bin/env bash
set -u

src=/tmp/audit-work/38-decode-cyclic-audit/candidate-src
trusted=/tmp/audit-work/38-decode-cyclic-audit/trusted
concrete=/tmp/audit-work/38-decode-cyclic-audit/build-concrete/semantic-llvm-kompiled
proof=/tmp/audit-work/38-decode-cyclic-audit/build-proof/verification-kompiled
regenerated=/tmp/audit-work/38-decode-cyclic-audit/build-concrete/solution.trusted-regenerated.mpy
overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then overall=1; fi
}

printf 'Fresh source-only reconstruction; no candidate kompiled directory is used.\n'
run kompile --version
run kprove --version
run krun --version
run python3 --version

printf '\n$ python3 %s %s > %s\n' \
  "$trusted/py2mpy.py" "$src/solution.py" "$regenerated"
python3 "$trusted/py2mpy.py" "$src/solution.py" > "$regenerated"
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

run cmp "$regenerated" "$src/solution.mpy"
run sha256sum "$regenerated" "$src/solution.mpy"

run kompile "$src/semantic.k" \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$concrete"

run kompile "$src/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof"

run test -f "$concrete/definition.kore"
run test -f "$proof/definition.kore"

printf '\nOverall fresh-build status: %d\n' "$overall"
exit "$overall"
