#!/usr/bin/env bash
set -u

project=/tmp/audit-work/stage5-mut-pymod-constant0-correct
toolchain=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LD_PRELOAD=/tmp/audit-work/lean_proc_compat.so
export PATH="$toolchain/bin:$PATH"
export LEAN="$toolchain/bin/lean"
export LEAN_SYSROOT="$toolchain/"
export LAKE_HOME="$toolchain/"
export LAKE_OVERRIDE_LEAN=1

echo '$ rg -n "def .*pyMod|  0$" Proof.lean'
(cd "$project" && rg -n 'def .*pyMod|  0$' Proof.lean)

echo '$ lake clean'
(cd "$project" && lake clean)
clean_status=$?
echo "mutation_lake_clean_exit=$clean_status"
test "$clean_status" -eq 0 || exit "$clean_status"

echo '$ lake build'
(cd "$project" && lake build)
build_status=$?
echo "mutation_lake_build_exit=$build_status"
test "$build_status" -eq 0 || exit "$build_status"

echo '$ cp /audit-output/evidence/MutationPyModCheck.lean MutationPyModCheck.lean'
cp /audit-output/evidence/MutationPyModCheck.lean "$project/MutationPyModCheck.lean"
echo '$ lake env lean MutationPyModCheck.lean'
set +e
(cd "$project" && lake env lean MutationPyModCheck.lean)
check_status=$?
set -e
echo "mutation_operational_check_exit=$check_status"
if [ "$check_status" -eq 0 ]; then
  echo 'ERROR: operational counterexample unexpectedly passed'
  exit 1
fi
echo 'EXPECTED FAILURE: the structurally provable constant-zero bridge violates frozen modulo behavior'
