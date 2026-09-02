#!/usr/bin/env bash
set -euo pipefail
set -x

for log in \
  stage1-integrity.log \
  stage1-trace-summary.log \
  prepare-scratch.log \
  stage2-fidelity.log \
  stage2-differential.log \
  stage3-kompile-llvm.log \
  stage3-kompile-haskell.log \
  stage4-witness.log \
  stage4-concrete.log \
  stage4-ast-pin.log \
  stage5-inventory.log \
  stage5-static-scan.log \
  stage6-dry-run.log \
  stage7-k-differential.log; do
  rg -q '^EXIT_STATUS: 0$' "/audit-output/evidence/$log"
done

for log in stage3-kprove-inner.log stage3-kprove-outer.log stage3-kprove-entry.log; do
  rg -q '^#Top$' "/audit-output/evidence/$log"
  rg -q '^EXIT_STATUS: 0$' "/audit-output/evidence/$log"
done

rg -q 'WarnStuckClaimState' /audit-output/evidence/stage6-kprove-false-empty.log
rg -q 'false ~> \.K' /audit-output/evidence/stage6-kprove-false-empty.log
rg -q '^EXIT_STATUS: 1$' /audit-output/evidence/stage6-kprove-false-empty.log

test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" = 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" = 1
diff -u <(printf 'VERDICT: CONCERNS\nLEGITIMACY: LEGIT\n') <(tail -n 2 /audit-output/REVIEW.md)

python3 -c 'import re; from pathlib import Path; p=Path("/audit-output/REVIEW.md"); missing=[x for x in re.findall(r"\]\((evidence/[^)]+)\)", p.read_text()) if not (p.parent/x).exists()]; print(f"missing_review_links={missing}"); raise SystemExit(bool(missing))'
