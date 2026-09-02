#!/usr/bin/env bash
set -u

root=/tmp/audit-work/38-decode-cyclic-audit
definition=$root/build-proof/verification-kompiled
overall=0

printf 'Haskell proof-definition witness: full submitted program\n'
printf '$ krun %q -cS=%q --definition %q\n' \
  "$root/candidate-src/solution.mpy" '"中"' "$definition"
full=$(krun "$root/candidate-src/solution.mpy" \
  -cS='"中"' --definition "$definition" 2>&1)
status=$?
printf '%s\n[exit %d]\n' "$full" "$status"
if [ "$status" -ne 0 ] || ! printf '%s' "$full" | rg -Fq 'pyStr ( "\xad\xe4\xb8" )'; then
  overall=1
fi

printf '\nHaskell proof-definition witness: focused len program\n'
printf '$ krun %q -cS=%q --definition %q\n' \
  "$root/unicode-witnesses/len_program.mpy" '"中"' "$definition"
length=$(krun "$root/unicode-witnesses/len_program.mpy" \
  -cS='"中"' --definition "$definition" 2>&1)
status=$?
printf '%s\n[exit %d]\n' "$length" "$status"
if [ "$status" -ne 0 ] || ! printf '%s' "$length" | rg -Fq 'pyInt ( 3 )'; then
  overall=1
fi

printf '\nPython facts: decode_cyclic("中") == "中"; len("中") == 1.\n'
printf 'Overall backend-consistency witness status: %d\n' "$overall"
exit "$overall"
