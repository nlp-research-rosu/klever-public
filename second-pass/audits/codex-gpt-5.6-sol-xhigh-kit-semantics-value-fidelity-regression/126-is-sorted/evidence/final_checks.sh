#!/usr/bin/env bash
set -u

echo "== REVIEW exact terminal markers =="
tail -n 2 /audit-output/REVIEW.md
verdict_count=$(grep -c '^VERDICT:' /audit-output/REVIEW.md)
legitimacy_count=$(grep -c '^LEGITIMACY:' /audit-output/REVIEW.md)
echo "verdict_marker_count=$verdict_count"
echo "legitimacy_marker_count=$legitimacy_count"
test "$verdict_count" -eq 1
test "$legitimacy_count" -eq 1
test "$(tail -n 2 /audit-output/REVIEW.md | sed -n '1p')" = "VERDICT: CONCERNS"
test "$(tail -n 1 /audit-output/REVIEW.md)" = "LEGITIMACY: LEGIT"
echo "terminal_markers_valid=$?"

echo "== positive proof signals =="
grep -E '^#Top$|^EXIT_STATUS:' \
  /audit-output/evidence/stage3-kprove-loop-invariant.log \
  /audit-output/evidence/stage3-kprove-full-spec.log

echo "== negative proof signals =="
grep -E 'WarnStuckClaimState|EXIT_STATUS:' \
  /audit-output/evidence/stage4-body-sensitivity-proof.log \
  /audit-output/evidence/stage6-nonvacuity-proof.log

echo "== final artifact types =="
stat -c '%F %s %n' /audit-output/REVIEW.md
find /audit-output/evidence -type l -printf 'SYMLINK %p -> %l\n'

echo "== evidence hashes (manifest log excluded to avoid self-reference) =="
find /audit-output/evidence -type f \
  ! -name final-audit-checks.log -print0 \
  | LC_ALL=C sort -z | xargs -0 sha256sum
