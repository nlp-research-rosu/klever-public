#!/usr/bin/env bash
set -u

record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return "$status"
}

overall=0

record test -d /reference/reference-semantics || overall=1
record test -d /candidate/reference-semantics || overall=1
record bash -c 'find /reference/reference-semantics -type l -print' || overall=1
record bash -c 'find /candidate/reference-semantics -type l -print' || overall=1
record diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics || overall=1
record cmp /reference/prompt.py /candidate/prompt.py || overall=1
record cmp /reference/py2mpy.py /candidate/py2mpy.py || overall=1

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy verification.k spec.k
do
  record test -f "/candidate/$artifact" || overall=1
  record test ! -L "/candidate/$artifact" || overall=1
done

record bash -c \
  'find /reference/reference-semantics -printf "%y %P -> %l\n" | LC_ALL=C sort' \
  || overall=1
record bash -c \
  'find /candidate/reference-semantics -printf "%y %P -> %l\n" | LC_ALL=C sort' \
  || overall=1
record sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/verification.k /candidate/spec.k \
  || overall=1
record bash -c \
  'find /reference/reference-semantics -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum' \
  || overall=1
record bash -c \
  'find /candidate/reference-semantics -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum' \
  || overall=1

record python3 - /candidate/run-input.json /candidate/metrics.json <<'PY' || overall=1
import json
import pathlib
import sys

for name in sys.argv[1:]:
    path = pathlib.Path(name)
    data = json.loads(path.read_text())
    print(f"{path.name}: {json.dumps(data, indent=2, sort_keys=True)}")
PY

record python3 - /candidate/codex-trace <<'PY' || overall=1
import collections
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
files = sorted(root.rglob("*.jsonl"))
print(f"trace_files={len(files)}")
for path in files:
    counts = collections.Counter()
    lines = 0
    parse_errors = 0
    first_timestamp = None
    last_timestamp = None
    for raw in path.open():
        lines += 1
        try:
            item = json.loads(raw)
        except json.JSONDecodeError:
            parse_errors += 1
            continue
        counts[item.get("type", "<missing>")] += 1
        timestamp = item.get("timestamp")
        if first_timestamp is None:
            first_timestamp = timestamp
        last_timestamp = timestamp
    print(
        f"{path}: bytes={path.stat().st_size} lines={lines} "
        f"parse_errors={parse_errors} first={first_timestamp} last={last_timestamp}"
    )
    print(f"record_types={dict(sorted(counts.items()))}")
PY

printf 'OVERALL_STATUS: %d\n' "$overall"
exit "$overall"
