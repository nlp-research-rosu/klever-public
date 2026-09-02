#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md
status=0

echo '$ tail -n 2 /audit-output/REVIEW.md'
tail -n 2 "$review"
tail_status=$?
echo "exit=$tail_status"
status=$((status | tail_status))

echo '$ test "$(tail -n 2 REVIEW.md)" = expected marker pair'
if test "$(tail -n 2 "$review")" = $'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'; then
  marker_status=0
else
  marker_status=1
fi
echo "exit=$marker_status"
status=$((status | marker_status))

echo '$ check all REVIEW.md evidence links exist'
python3 - <<'PY'
import re
from pathlib import Path

review = Path("/audit-output/REVIEW.md").read_text(encoding="utf-8")
links = sorted(set(re.findall(r"\]\((evidence/[^)]+)\)", review)))
missing = [link for link in links if not (Path("/audit-output") / link).exists()]
print(f"evidence_links={len(links)}")
print(f"missing_links={len(missing)}")
for link in missing:
    print(link)
raise SystemExit(bool(missing))
PY
link_status=$?
echo "exit=$link_status"
status=$((status | link_status))

echo '$ verify positive proof success signals'
for log in stage3-kprove-loop.log stage3-kprove-entry.log; do
  if rg -q '^#Top$' "/audit-output/evidence/$log" &&
     rg -q '^exit=0$' "/audit-output/evidence/$log"; then
    echo "$log: #Top and exit=0"
  else
    echo "$log: missing success signal"
    status=1
  fi
done

echo '$ verify false mutation failure signals'
if rg -q 'WarnStuckClaimState' /audit-output/evidence/stage6-mutation-proof.log &&
   rg -q '^exit=1$' /audit-output/evidence/stage6-mutation-proof.log; then
  echo 'stage6-mutation-proof.log: stuck claim and exit=1'
else
  echo 'stage6-mutation-proof.log: missing expected failure signal'
  status=1
fi

echo "final_validation_exit=$status"
exit "$status"
