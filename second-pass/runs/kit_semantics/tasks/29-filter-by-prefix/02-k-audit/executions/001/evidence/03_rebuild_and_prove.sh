#!/usr/bin/env bash
set -u

work=/tmp/audit-work/work
fail=0
cd "$work" || exit 1

run_step() {
  description="$1"
  shift
  echo
  echo "COMMAND: $*"
  "$@"
  status=$?
  echo "EXIT[$description]=$status"
  if test "$status" -ne 0; then
    fail=1
  fi
}

echo 'COMMAND: bash /audit-output/evidence/03_rebuild_and_prove.sh'
echo '== Initial scratch definition/cache check =='
find . -maxdepth 1 \( -name '*-kompiled' -o -name '.kompile-*' -o -name '*.bin' \) -print

run_step kompile-version kompile --version
run_step kprove-version kprove --version
run_step krun-version krun --version

echo
echo '== Fresh trusted concrete definition and execution =='
echo 'COMMAND: python3 /reference/py2mpy.py auditor-concrete.py > auditor-concrete.mpy'
python3 /reference/py2mpy.py auditor-concrete.py > auditor-concrete.mpy
status=$?
echo "EXIT[translate-concrete]=$status"
if test "$status" -ne 0; then fail=1; fi
run_step llvm-build \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition auditor-runtime-kompiled
run_step concrete-krun \
  krun auditor-concrete.mpy \
    --definition auditor-runtime-kompiled \
    --output pretty

echo
echo '== Bridge-free iterator connection definition and claim =='
run_step connection-build \
  kompile --backend haskell domain.k \
    --main-module STRING-SEQUENCE-DOMAIN \
    --syntax-module MPY-SYNTAX \
    --output-definition auditor-connection-kompiled
run_step connection-claim \
  kprove connection-spec.k \
    --definition auditor-connection-kompiled \
    --spec-module CONNECTION-SPEC \
    --claims CONNECTION-SPEC.string-iterator-normalization

echo
echo '== Bridge-free loop connection definition and claim =='
run_step loop-connection-build \
  kompile --backend haskell verification-core.k \
    --main-module VERIFICATION-CORE \
    --syntax-module MPY-SYNTAX \
    --output-definition auditor-loop-connection-kompiled
run_step loop-connection-claim \
  kprove loop-connection-spec.k \
    --definition auditor-loop-connection-kompiled \
    --spec-module LOOP-CONNECTION-SPEC \
    --claims LOOP-CONNECTION-SPEC.filter-loop-connection

echo
echo '== Final proof definition, constructor identity, and target claims =='
run_step verification-build \
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition auditor-verification-kompiled

echo 'COMMAND: kast solution.mpy --definition auditor-verification-kompiled --module VERIFICATION --sort Module --output kore > auditor-program-source.kore'
kast solution.mpy \
  --definition auditor-verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore > auditor-program-source.kore
status=$?
echo "EXIT[kast-source]=$status"
if test "$status" -ne 0; then fail=1; fi

echo "COMMAND: kast --expression filterByPrefixProgram --definition auditor-verification-kompiled --module VERIFICATION --sort Module --expand-macros --output kore > auditor-program-macro.kore"
kast \
  --expression filterByPrefixProgram \
  --definition auditor-verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > auditor-program-macro.kore
status=$?
echo "EXIT[kast-macro]=$status"
if test "$status" -ne 0; then fail=1; fi

run_step constructor-cmp cmp -s auditor-program-source.kore auditor-program-macro.kore
sha256sum auditor-program-source.kore auditor-program-macro.kore
wc -c auditor-program-source.kore auditor-program-macro.kore

run_step target-filter-loop \
  kprove spec.k \
    --definition auditor-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.filter-loop
run_step target-filter-program \
  kprove spec.k \
    --definition auditor-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.filter-program
run_step target-all-claims \
  kprove spec.k \
    --definition auditor-verification-kompiled \
    --spec-module SPEC

echo
echo "SCRIPT_EXIT=$fail"
exit "$fail"
