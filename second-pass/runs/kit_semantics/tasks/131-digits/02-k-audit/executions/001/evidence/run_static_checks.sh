#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/source || exit 90

echo '$ rg -n "^[[:space:]]*(syntax|rule)" verification.k'
rg -n '^[[:space:]]*(syntax|rule)' verification.k
inventory_status=$?
echo "EXIT_STATUS=$inventory_status"

echo '$ rg -n "<k>|priority|owise|concrete|no-evaluators|functional" verification.k'
rg -n '<k>|priority|owise|concrete|no-evaluators|functional' verification.k
bridge_search_status=$?
echo "EXIT_STATUS=$bridge_search_status EXPECTED_NO_MATCH=1"

echo '$ rg -n "no-evaluators|md5hexCodes|sortVS|sortKeyVS|Float|float" solution.mpy spec.k verification.k'
rg -n 'no-evaluators|md5hexCodes|sortVS|sortKeyVS|Float|float' \
  solution.mpy spec.k verification.k
opaque_use_status=$?
echo "EXIT_STATUS=$opaque_use_status EXPECTED_NO_MATCH=1"

echo '$ rg -n "MPY-CONCRETE|MPY-KRUN" verification.k spec.k'
rg -n 'MPY-CONCRETE|MPY-KRUN' verification.k spec.k
concrete_import_status=$?
echo "EXIT_STATUS=$concrete_import_status EXPECTED_NO_MATCH=1"

echo '$ rg -n -i "ksort" /tmp/audit-work/rebuilt-verification-kompiled/definition.kore'
rg -n -i 'ksort' \
  /tmp/audit-work/rebuilt-verification-kompiled/definition.kore
haskell_ksort_status=$?
echo "EXIT_STATUS=$haskell_ksort_status EXPECTED_NO_MATCH=1"

echo '$ rg -n -i "ksort" /tmp/audit-work/rebuilt-runtime-kompiled/definition.kore | sed -n "1,3p"'
rg -n -i 'ksort' \
  /tmp/audit-work/rebuilt-runtime-kompiled/definition.kore \
  | sed -n '1,3p'
llvm_ksort_status=${PIPESTATUS[0]}
echo "EXIT_STATUS=$llvm_ksort_status EXPECTED_MATCH=0"

test "$inventory_status" -eq 0 \
  && test "$bridge_search_status" -eq 1 \
  && test "$opaque_use_status" -eq 1 \
  && test "$concrete_import_status" -eq 1 \
  && test "$haskell_ksort_status" -eq 1 \
  && test "$llvm_ksort_status" -eq 0
