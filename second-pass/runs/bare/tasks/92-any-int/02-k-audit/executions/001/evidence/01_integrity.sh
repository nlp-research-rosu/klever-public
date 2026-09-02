#!/usr/bin/env bash
set -u

log=/audit-output/evidence/01_integrity.log
exec > >(tee "$log") 2>&1

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'AUDIT_STAGE: 1 input and provenance integrity\n'
run find /candidate -maxdepth 5 -printf '%y %p -> %l\n'
run find /reference -maxdepth 3 -printf '%y %p -> %l\n'
run bash -c 'if [ -e /reference/reference-semantics ] || [ -L /reference/reference-semantics ]; then echo MODE_INTEGRITY_BREACH; exit 1; else echo MODE_INTEGRITY_OK_GENERATED_SEMANTICS; fi'
run sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run stat -c '%F %s bytes %n' /candidate/run-input.json /candidate/metrics.json /candidate/codex-last.txt /candidate/codex-output.log /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-10-07-019f8984-c566-7aa2-b4a8-d0f068cabf14.jsonl
run wc -lc /candidate/run-input.json /candidate/metrics.json /candidate/codex-last.txt /candidate/codex-output.log /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-10-07-019f8984-c566-7aa2-b4a8-d0f068cabf14.jsonl
run sed -n 1,80p /candidate/run-input.json
run sed -n 1,80p /candidate/metrics.json
run sed -n 1,80p /candidate/codex-last.txt
run bash -c 'set -o pipefail; rg -n "RESULT:|#Top|kprove|kompile|krun|WarnStuck|error|failed" /candidate/codex-output.log | tail -n 80'
run bash -c 'python3 - "$1" <<'"'"'PY'"'"'
import json
import sys
from collections import Counter

path = sys.argv[1]
types = Counter()
events = 0
first = None
last = None
with open(path, encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        events += 1
        types[record.get("type", "<missing>")] += 1
        if first is None:
            first = (line_number, record.get("timestamp"), record.get("type"))
        last = (line_number, record.get("timestamp"), record.get("type"))
print(f"validated_jsonl_events={events}")
print(f"event_types={dict(sorted(types.items()))}")
print(f"first={first}")
print(f"last={last}")
PY' _ /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-10-07-019f8984-c566-7aa2-b4a8-d0f068cabf14.jsonl
