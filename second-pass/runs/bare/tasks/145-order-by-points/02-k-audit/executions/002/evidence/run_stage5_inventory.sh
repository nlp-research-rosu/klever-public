#!/usr/bin/env bash
set -u
set -x

nl -ba /candidate/semantic.k
semantic_numbering_rc=$?
nl -ba /candidate/verification.k
verification_numbering_rc=$?
nl -ba /candidate/spec.k
spec_numbering_rc=$?

rg -n '^[[:space:]]*(syntax|configuration|rule|claim)([[:space:]]|$)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
declaration_scan_rc=$?

rg -n '\[(function|total|functional|simplification|concrete|priority|owise|symbol|anywhere)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
attribute_scan_rc=$?

set +x
printf 'semantic_numbering_exit=%d\n' "$semantic_numbering_rc"
printf 'verification_numbering_exit=%d\n' "$verification_numbering_rc"
printf 'spec_numbering_exit=%d\n' "$spec_numbering_rc"
printf 'declaration_scan_exit=%d\n' "$declaration_scan_rc"
printf 'attribute_scan_exit=%d\n' "$attribute_scan_rc"
test "$semantic_numbering_rc" -eq 0 \
  && test "$verification_numbering_rc" -eq 0 \
  && test "$spec_numbering_rc" -eq 0 \
  && test "$declaration_scan_rc" -eq 0 \
  && test "$attribute_scan_rc" -eq 0
