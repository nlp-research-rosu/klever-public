#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md
evidence=/audit-output/evidence

echo '$ rg -n "^## [1-7]\\." /audit-output/REVIEW.md'
rg -n '^## [1-7]\.' "$review"
heading_status=$?
echo "EXIT_STATUS=$heading_status"

echo '$ tail -n 2 /audit-output/REVIEW.md'
tail -n 2 "$review"
tail_status=$?
echo "EXIT_STATUS=$tail_status"

expected=$'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'
actual="$(tail -n 2 "$review")"
if [[ "$actual" == "$expected" ]]; then
  marker_status=0
else
  marker_status=1
fi
echo "FINAL_MARKERS_EXACT=$((1 - marker_status))"

echo '$ bash -n /audit-output/evidence/*.sh'
bash_status=0
for script in "$evidence"/*.sh; do
  bash -n "$script" || bash_status=1
done
echo "EXIT_STATUS=$bash_status"

echo '$ python3 -c <AST-parse every reviewer Python script>'
python3 - "$evidence" <<'PY'
import ast
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
paths = sorted(root.glob("*.py"))
for path in paths:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
print(f"AST_PARSED={len(paths)}")
PY
python_status=$?
echo "EXIT_STATUS=$python_status"

if [[ "$heading_status" -ne 0 || "$tail_status" -ne 0 ||
      "$marker_status" -ne 0 || "$bash_status" -ne 0 ||
      "$python_status" -ne 0 ]]; then
  exit 1
fi
exit 0
