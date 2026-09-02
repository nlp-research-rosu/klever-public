#!/usr/bin/env bash
set -u

status=0

printf '%s\n' '$ python3 -m json.tool /candidate/run-input.json'
python3 -m json.tool /candidate/run-input.json
rc=$?
printf 'run_input_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ python3 -m json.tool /candidate/metrics.json'
python3 -m json.tool /candidate/metrics.json
rc=$?
printf 'metrics_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ nl -ba /candidate/codex-last.txt'
nl -ba /candidate/codex-last.txt
rc=$?
printf 'codex_last_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ bounded codex-output.log head and tail'
sed -n '1,30p' /candidate/codex-output.log
printf '%s\n' '[... bounded omission ...]'
tail -60 /candidate/codex-output.log
rc=$?
printf 'codex_output_bounded_read_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ structured generation trace hashes and record-type counts'
find /candidate/codex-trace -type f -print0 | sort -z | xargs -0 sha256sum
rc=$?
printf 'trace_hash_exit=%d\n' "$rc"
(( rc == 0 )) || status=1
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path

paths = sorted(Path("/candidate/codex-trace").rglob("*"))
files = [path for path in paths if path.is_file()]
print(f"trace_file_count={len(files)}")
for path in files:
    counts = Counter()
    records = 0
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            obj = json.loads(line)
            records += 1
            counts[obj.get("type", "<none>")] += 1
    print(f"{path}: records={records} types={dict(counts)}")
PY
rc=$?
printf 'trace_parse_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ sha256sum untrusted provenance artifacts'
sha256sum \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log
rc=$?
printf 'provenance_hash_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf 'overall_exit=%d\n' "$status"
exit "$status"
