#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive/candidate-src
cd "$work" || exit 90

python3 /tmp/audit-work/30-get-positive/trusted/py2mpy.py \
  solution-threshold-one.py > solution-threshold-one.mpy
translation_status=$?
printf 'STATUS body_mutation_translation=%s\n' "$translation_status"
printf 'BODY_MUTATION translated_term:\n'
sed -n '1,80p' solution-threshold-one.mpy

kprove spec-body-sensitivity.k \
  --definition proof-kompiled \
  --spec-module SPEC-BODY-SENSITIVITY \
  --claims SPEC-BODY-SENSITIVITY.changed-threshold
body_status=$?
printf 'STATUS body_sensitivity_expected_nonzero=%s\n' "$body_status"

kompile continuation-test.k \
  --backend haskell \
  --main-module CONTINUATION-TEST \
  --syntax-module MPY-SYNTAX \
  --output-definition continuation-kompiled
continuation_build_status=$?
printf 'STATUS continuation_build=%s\n' "$continuation_build_status"

kprove continuation-spec.k \
  --definition continuation-kompiled \
  --spec-module CONTINUATION-SPEC \
  --claims CONTINUATION-SPEC.suffix-preserved
continuation_status=$?
printf 'STATUS continuation_proof=%s\n' "$continuation_status"

if [ "$translation_status" -eq 0 ] \
  && [ "$body_status" -ne 0 ] \
  && [ "$continuation_build_status" -eq 0 ] \
  && [ "$continuation_status" -eq 0 ]; then
  exit 0
fi
exit 1
