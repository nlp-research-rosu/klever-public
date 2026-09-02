#!/usr/bin/env bash
set -u
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

test ! -e /reference/reference-semantics
find /candidate -maxdepth 3 -printf '%y %p -> %l\n' | sort
find /reference -maxdepth 3 -printf '%y %p -> %l\n' | sort
find /candidate -type l -printf '%p -> %l\n'
find /candidate ! -type f ! -type d ! -type l -printf '%y %p\n'

sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
cmp -s /candidate/prompt.py /reference/prompt.py
printf 'prompt_cmp_exit=%s\n' "$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'translator_cmp_exit=%s\n' "$?"

python3 -m json.tool /candidate/run-input.json
python3 -m json.tool /candidate/metrics.json
wc -l -c /candidate/codex-last.txt /candidate/codex-output.log
sed -n '1,80p' /candidate/codex-last.txt
sed -n '1,80p' /candidate/codex-output.log
tail -80 /candidate/codex-output.log

trace_file="$(find /candidate/codex-trace -type f -name '*.jsonl' | head -1)"
python3 - "$trace_file" <<'PY'
import collections
import json
import sys

path = sys.argv[1]
counts = collections.Counter()
with open(path, encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        try:
            item = json.loads(line)
        except Exception as error:
            print(f"INVALID line={line_number}: {error}")
            raise
        counts[item.get("type", "(no type)")] += 1
print("valid_jsonl=true")
print("record_count=", sum(counts.values()))
print("types=", dict(sorted(counts.items())))
PY

command -v kompile
command -v krun
command -v kprove
command -v kast
kompile --version
kprove --version
