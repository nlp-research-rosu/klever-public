#!/usr/bin/env bash
set -u

echo '$ test ! -e /reference/reference-semantics'
test ! -e /reference/reference-semantics
status=$?
echo "exit_status=$status"

echo '$ for p in run-input.json metrics.json codex-last.txt codex-output.log prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k spec.k prove.sh; do test -f /candidate/$p && test ! -L /candidate/$p; done'
status=0
for p in run-input.json metrics.json codex-last.txt codex-output.log prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k spec.k prove.sh; do
  if test ! -f "/candidate/$p" || test -L "/candidate/$p"; then
    echo "bad_required_artifact=$p"
    status=1
  fi
done
echo "exit_status=$status"

echo '$ find /candidate -type l -printf "%p -> %l\n"'
find /candidate -type l -printf '%p -> %l\n'
status=$?
echo "exit_status=$status"

echo '$ sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py'
sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py
status=$?
echo "exit_status=$status"

echo '$ cmp -s /reference/prompt.py /candidate/prompt.py'
cmp -s /reference/prompt.py /candidate/prompt.py
status=$?
echo "exit_status=$status"

echo '$ cmp -s /reference/py2mpy.py /candidate/py2mpy.py'
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
status=$?
echo "exit_status=$status"

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T07-38-42-019f89d5-dfc5-77c1-aedf-b8b83744126d.jsonl
echo '$ python3 -m json.tool /candidate/run-input.json >/dev/null'
python3 -m json.tool /candidate/run-input.json >/dev/null
status=$?
echo "exit_status=$status"

echo '$ python3 -m json.tool /candidate/metrics.json >/dev/null'
python3 -m json.tool /candidate/metrics.json >/dev/null
status=$?
echo "exit_status=$status"

echo '$ python3 -c <validate every JSONL record in structured trace>'
python3 - "$trace" <<'PY'
import json
import sys
from collections import Counter

counts = Counter()
with open(sys.argv[1], encoding="utf-8") as stream:
    for number, line in enumerate(stream, 1):
        obj = json.loads(line)
        counts[obj.get("type", "<missing>")] += 1
print(f"valid_records={sum(counts.values())}")
print(f"record_types={dict(sorted(counts.items()))}")
PY
status=$?
echo "exit_status=$status"

exit "$status"
