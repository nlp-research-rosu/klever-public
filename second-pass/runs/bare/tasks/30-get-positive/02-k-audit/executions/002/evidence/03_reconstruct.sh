#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive/candidate-src
cd "$work" || exit 90

kompile --version
kprove --version
krun --version

kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
concrete_build_status=$?
printf 'STATUS concrete_build=%s\n' "$concrete_build_status"

kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
proof_build_status=$?
printf 'STATUS proof_build=%s\n' "$proof_build_status"

printf 'CONCRETE case=example_one python_expected=[2,5,6]\n'
krun solution.mpy \
  --definition concrete-kompiled \
  -cINPUT='cons(-1, cons(2, cons(-4, cons(5, cons(6, nil)))))'
concrete_example_status=$?
printf 'STATUS concrete_example_one=%s\n' "$concrete_example_status"

printf 'CONCRETE case=empty python_expected=[]\n'
krun solution.mpy \
  --definition concrete-kompiled \
  -cINPUT='nil'
concrete_empty_status=$?
printf 'STATUS concrete_empty=%s\n' "$concrete_empty_status"

printf 'CONCRETE case=boundary python_expected=[1,2,2]\n'
krun solution.mpy \
  --definition concrete-kompiled \
  -cINPUT='cons(-2, cons(-1, cons(0, cons(1, cons(2, cons(2, nil))))))'
concrete_boundary_status=$?
printf 'STATUS concrete_boundary=%s\n' "$concrete_boundary_status"

printf 'CONCRETE case=all_nonpositive python_expected=[]\n'
krun solution.mpy \
  --definition concrete-kompiled \
  -cINPUT='cons(0, cons(-1, cons(-999999999999999999999999999999, nil)))'
concrete_nonpositive_status=$?
printf 'STATUS concrete_all_nonpositive=%s\n' "$concrete_nonpositive_status"

printf 'CONCRETE case=large_positive python_expected=[999999999999999999999999999999]\n'
krun solution.mpy \
  --definition concrete-kompiled \
  -cINPUT='cons(999999999999999999999999999999, nil)'
concrete_large_status=$?
printf 'STATUS concrete_large_positive=%s\n' "$concrete_large_status"

exit "$((concrete_build_status || proof_build_status || concrete_example_status || concrete_empty_status || concrete_boundary_status || concrete_nonpositive_status || concrete_large_status))"
