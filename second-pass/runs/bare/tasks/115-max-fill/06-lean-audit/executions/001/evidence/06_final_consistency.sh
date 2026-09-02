#!/usr/bin/env bash
set -u
echo '$ tail -n 2 /audit-output/REVIEW.md'
tail -n 2 /audit-output/REVIEW.md
echo '$ grep -c "^VERDICT:" /audit-output/REVIEW.md'
grep -c '^VERDICT:' /audit-output/REVIEW.md
echo '$ grep -c "^LEGITIMACY:" /audit-output/REVIEW.md'
grep -c '^LEGITIMACY:' /audit-output/REVIEW.md
echo '$ python3 -m json.tool /audit-output/evidence/04_preflight_return.json'
python3 -m json.tool /audit-output/evidence/04_preflight_return.json
echo '$ sha256sum /audit-output/REVIEW.md'
sha256sum /audit-output/REVIEW.md
echo '$ find /audit-output/evidence -maxdepth 1 -type f -printf "%f\n" | sort'
find /audit-output/evidence -maxdepth 1 -type f -printf '%f\n' | sort
