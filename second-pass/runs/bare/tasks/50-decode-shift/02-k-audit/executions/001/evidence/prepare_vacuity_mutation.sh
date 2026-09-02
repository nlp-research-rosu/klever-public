#!/usr/bin/env bash
set -u

source_mutation=/audit-output/evidence/spec-vacuity.k
scratch_mutation=/tmp/audit-work/50-decode-shift/candidate-src/spec-vacuity.k

cp -- "$source_mutation" "$scratch_mutation"
cmp -s "$source_mutation" "$scratch_mutation"
status=$?
printf 'COPY_BYTE_IDENTITY_STATUS\t%s\n' "$status"
sha256sum "$source_mutation" "$scratch_mutation"
printf 'FALSE_WITNESS\tCS=cons(102,nil), allLower=true, decode result=cons(97,nil), mutated encodeSpec result=cons(107,nil)\n'
exit "$status"
