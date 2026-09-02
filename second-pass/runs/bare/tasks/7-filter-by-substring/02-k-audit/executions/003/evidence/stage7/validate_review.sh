#!/usr/bin/env bash
set -u

status=0

printf '%s\n' '$ python3 - (validate exact REVIEW.md terminator)'
python3 - <<'PY'
from pathlib import Path

path = Path("/audit-output/REVIEW.md")
text = path.read_text(encoding="utf-8")
assert text.splitlines()[-2:] == [
    "VERDICT: FAIL",
    "LEGITIMACY: NOT_LEGIT",
]
assert text.endswith("VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT\n")
assert sum(line.startswith("VERDICT:") for line in text.splitlines()) == 1
assert sum(line.startswith("LEGITIMACY:") for line in text.splitlines()) == 1
print("review_terminator_valid=true")
PY
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ bash -n evidence/**/*.sh'
while IFS= read -r script; do
  bash -n "$script"
  rc=$?
  printf '%s EXIT: %d\n' "$script" "$rc"
  if [[ "$rc" -ne 0 ]]; then
    status=1
  fi
done < <(find /audit-output/evidence -type f -name '*.sh' | sort)

printf '%s\n' '$ python3 - (compile reviewer Python scripts in memory)'
python3 - <<'PY'
from pathlib import Path

for path in sorted(Path("/audit-output/evidence").rglob("*.py")):
    compile(path.read_text(encoding="utf-8"), str(path), "exec")
    print(f"{path} COMPILE: 0")
PY
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ PYTHONPATH=/opt/humaneval/tools python3 - (candidate tree unchanged)'
PYTHONPATH=/opt/humaneval/tools python3 - <<'PY'
from pathlib import Path

import pipeline_contract

actual = pipeline_contract.sha256_tree(Path("/candidate"))
expected = "e0fb514f85cefa15af6d674efc35a7f462d9600eb8cd68b72f86ce587b371048"
print(f"candidate_sha256_tree={actual}")
print(f"matches_generation_workspace={actual == expected}")
assert actual == expected
PY
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

printf '%s\n' '$ find /audit-output/evidence -type f -printf "%s %p\\n" | sort -k2'
find /audit-output/evidence -type f -printf '%s %p\n' | sort -k2
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

exit "$status"
