#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/body-mutation
BUILD=/tmp/audit-work/build/body-mutation-kompiled
EVIDENCE=/audit-output/evidence
status=0

printf '$ cp -a %s %s\n' \
  "$WORK/verification.k" "$EVIDENCE/body-mutation-verification.k"
cp -a "$WORK/verification.k" "$EVIDENCE/body-mutation-verification.k"
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi

printf '$ diff -u /tmp/audit-work/source/verification.k %s\n' \
  "$WORK/verification.k"
diff -u /tmp/audit-work/source/verification.k "$WORK/verification.k" \
  > "$EVIDENCE/stage5-body-mutation.diff"
diff_rc=$?
printf '[exit %d; expected 1 for different files]\n' "$diff_rc"
cat "$EVIDENCE/stage5-body-mutation.diff"
if (( diff_rc != 1 )); then status=1; fi

printf '$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition %s\n' \
  "$BUILD"
(cd "$WORK" && kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$BUILD") \
  > "$EVIDENCE/stage5-body-mutation-kompile.log" 2>&1
compile_rc=$?
printf '[exit %d]\n' "$compile_rc"
tail -100 "$EVIDENCE/stage5-body-mutation-kompile.log"
if (( compile_rc != 0 )); then status=1; fi

printf '$ kprove spec.k --definition %s --spec-module SPEC\n' "$BUILD"
(cd "$WORK" && kprove spec.k \
  --definition "$BUILD" \
  --spec-module SPEC) \
  > "$EVIDENCE/stage5-body-mutation-kprove.log" 2>&1
prove_rc=$?
printf '[exit %d; expected nonzero]\n' "$prove_rc"
tail -180 "$EVIDENCE/stage5-body-mutation-kprove.log"
if (( prove_rc == 0 )); then status=1; fi
if ! rg -q 'WarnStuckClaimState' "$EVIDENCE/stage5-body-mutation-kprove.log"; then
  status=1
fi

printf 'Final body_sensitivity_status=%d\n' "$status"
exit "$status"
