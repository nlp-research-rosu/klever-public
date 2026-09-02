#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/147-get-max-triples-clean || exit 1
status=0

record() {
  log=$1
  shift
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1 | tee "/audit-output/evidence/$log"
  rc=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

printf '$ cp reviewer Stage-4 artifacts to clean scratch\n'
cp /audit-output/evidence/adequacy_witness.py .
cp /audit-output/evidence/spec-witness.k .
cp /audit-output/evidence/verification-body-mutant.k .
cp /audit-output/evidence/spec-body-mutant.k .
printf '[exit 0]\n'

record adequacy-witness.log python3 adequacy_witness.py
if (( $? != 0 )); then status=1; fi

record kprove-entry-n5.log \
  kprove spec-witness.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-WITNESS \
  -I . \
  --output pretty
if (( $? != 0 )); then
  status=1
elif ! grep -Fxq '#Top' /audit-output/evidence/kprove-entry-n5.log; then
  printf '[missing exact #Top for entry-n5]\n'
  status=1
fi

record kompile-body-mutant.log \
  kompile verification-body-mutant.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mutant-kompiled \
  -I .
if (( $? != 0 )); then
  status=1
else
  printf '$ kprove changed-body claim (expected semantic failure)\n'
  record kprove-body-mutant.log \
    kprove spec-body-mutant.k \
    --definition verification-body-mutant-kompiled \
    --spec-module SPEC-BODY-MUTANT \
    -I . \
    --output pretty
  mutant_rc=$?
  if (( mutant_rc == 0 )); then
    printf '[unexpected success: changed executed body proved original result]\n'
    status=1
  elif ! rg -q 'WarnStuckClaimState|implication check.*failed|cannot be rewritten further' \
      /audit-output/evidence/kprove-body-mutant.log; then
    printf '[failure did not contain an expected unmet-obligation diagnostic]\n'
    status=1
  else
    printf '[expected semantic proof failure observed; audit condition satisfied]\n'
  fi
fi

printf 'FINAL_STATUS=%d\n' "$status"
exit "$status"
