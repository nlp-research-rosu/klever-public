#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/proof-audit.Dl0nBZ/candidate
export PATH="/home/agent/.nix-profile/bin:$PATH"

run_status() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd "$WORK" || exit 90

printf '## Tool versions\n'
run_status kompile --version
run_status kprove --version

printf '\n## Trusted translation of concrete test\n'
printf '$ python3 /reference/py2mpy.py concrete-tests.py > concrete-tests.mpy\n'
python3 /reference/py2mpy.py concrete-tests.py > concrete-tests.mpy
printf '[exit %d]\n' "$?"

printf '\n## Fresh concrete definition\n'
run_status kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

printf '\n## Concrete executions\n'
run_status krun solution.mpy --definition runtime-kompiled
run_status krun concrete-tests.mpy --definition runtime-kompiled

printf '\n## Fresh proof definition\n'
run_status kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

printf '\n## Original positive target claims together\n'
run_status kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

printf '\n## Labeled spec parse/dry run\n'
run_status kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module SPEC-LABELED \
  --dry-run

printf '\n## Loop target selected independently\n'
run_status kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module SPEC-LABELED \
  --claims loop

printf '\n## Entry target selected independently\n'
run_status kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module SPEC-LABELED \
  --claims entry
