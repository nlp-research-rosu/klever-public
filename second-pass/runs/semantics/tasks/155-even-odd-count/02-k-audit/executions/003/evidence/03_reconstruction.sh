#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

fresh=/tmp/audit-work/fresh
run find "$fresh" -maxdepth 2 -type d -o -type f || exit $?
run test ! -e "$fresh/runtime-kompiled" || exit $?
run test ! -e "$fresh/verification-base-kompiled" || exit $?
run test ! -e "$fresh/verification-kompiled" || exit $?
run cp /audit-output/evidence/03_concrete_tests.py "$fresh/audit-concrete-tests.py" || exit $?

printf '$ python3 /reference/py2mpy.py /tmp/audit-work/fresh/audit-concrete-tests.py > /tmp/audit-work/fresh/audit-concrete-tests.mpy\n'
python3 /reference/py2mpy.py "$fresh/audit-concrete-tests.py" > "$fresh/audit-concrete-tests.mpy"
status=$?
printf '[exit %d]\n' "$status"
test "$status" -eq 0 || exit "$status"

run env PATH="/home/agent/.nix-profile/bin:$PATH" \
  kompile "$fresh/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$fresh/runtime-kompiled" || exit $?

run env PATH="/home/agent/.nix-profile/bin:$PATH" \
  krun "$fresh/audit-concrete-tests.mpy" \
  --definition "$fresh/runtime-kompiled" || exit $?

run env PATH="/home/agent/.nix-profile/bin:$PATH" \
  kompile "$fresh/verification.k" \
  --backend haskell \
  --main-module EVEN-ODD-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$fresh/verification-base-kompiled" || exit $?

run env PATH="/home/agent/.nix-profile/bin:$PATH" \
  kprove "$fresh/spec.k" \
  --definition "$fresh/verification-base-kompiled" \
  --spec-module EVEN-ODD-LOOP-SPEC || exit $?

run env PATH="/home/agent/.nix-profile/bin:$PATH" \
  kompile "$fresh/verification.k" \
  --backend haskell \
  --main-module EVEN-ODD-VERIFICATION-SUMMARY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$fresh/verification-kompiled" || exit $?

run env PATH="/home/agent/.nix-profile/bin:$PATH" \
  kprove "$fresh/spec.k" \
  --definition "$fresh/verification-kompiled" \
  --spec-module EVEN-ODD-SPEC || exit $?
