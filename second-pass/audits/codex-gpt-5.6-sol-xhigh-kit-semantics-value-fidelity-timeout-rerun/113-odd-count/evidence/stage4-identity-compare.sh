#!/usr/bin/env bash
set -u

BUILD=/tmp/audit-work/build
EVIDENCE=/audit-output/evidence
status=0

printf '$ krun /tmp/audit-work/source/solution.mpy --definition %s --depth 0 --output json --output-file %s\n' \
  "$BUILD/identity-kompiled" "$EVIDENCE/stage4-solution-config.json"
krun /tmp/audit-work/source/solution.mpy \
  --definition "$BUILD/identity-kompiled" \
  --depth 0 \
  --output json \
  --output-file "$EVIDENCE/stage4-solution-config.json" \
  > "$EVIDENCE/stage4-solution-config.stderr.log" 2>&1
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi

printf '$ krun /audit-output/evidence/program-macro.mpy --definition %s --depth 0 --output json --output-file %s\n' \
  "$BUILD/identity-kompiled" "$EVIDENCE/stage4-macro-config.json"
krun "$EVIDENCE/program-macro.mpy" \
  --definition "$BUILD/identity-kompiled" \
  --depth 0 \
  --output json \
  --output-file "$EVIDENCE/stage4-macro-config.json" \
  > "$EVIDENCE/stage4-macro-config.stderr.log" 2>&1
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi

printf '$ cmp -s %s %s\n' \
  "$EVIDENCE/stage4-solution-config.json" "$EVIDENCE/stage4-macro-config.json"
cmp -s "$EVIDENCE/stage4-solution-config.json" "$EVIDENCE/stage4-macro-config.json"
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi

printf '$ sha256sum %s %s\n' \
  "$EVIDENCE/stage4-solution-config.json" "$EVIDENCE/stage4-macro-config.json"
sha256sum "$EVIDENCE/stage4-solution-config.json" "$EVIDENCE/stage4-macro-config.json"
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi

printf 'Final identity_status=%d\n' "$status"
exit "$status"
