#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf '\n$ python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/generated/solution-regenerated.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/generated/solution-regenerated.mpy
status=$?
printf '[exit %d]\n' "$status"

run cmp -s \
  /tmp/audit-work/generated/solution-regenerated.mpy \
  /tmp/audit-work/source/solution.mpy
run sha256sum \
  /tmp/audit-work/generated/solution-regenerated.mpy \
  /tmp/audit-work/source/solution.mpy

printf '\n$ python3 /audit-output/evidence/differential.py > /audit-output/evidence/differential-results.json\n'
python3 /audit-output/evidence/differential.py > /audit-output/evidence/differential-results.json
status=$?
printf '[exit %d]\n' "$status"

run python3 -c '
import json
p="/audit-output/evidence/differential-results.json"
d=json.load(open(p, encoding="utf-8"))
print({k:d[k] for k in ("oracle","candidate","seed","named_case_count","generated_case_count","mismatch_count")})
print("named_results=")
for r in d["records"][:d["named_case_count"]]:
    print(r["name"], r["canonical"], "match=", r["match"])
'
run sha256sum /audit-output/evidence/differential-results.json
