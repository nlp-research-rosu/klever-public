#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

echo "Trusted/candidate mount inventory (type, path, symlink target):"
run find /reference -maxdepth 3 -printf '%y %p -> %l\n'
run find /candidate -maxdepth 6 -printf '%y %p -> %l\n'

echo "Required provenance comparisons:"
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh

echo "Rendered GENERATED_SEMANTICS boundary:"
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  echo "reference/reference-semantics unexpectedly exists"
  boundary_status=1
else
  echo "reference/reference-semantics absent as required"
  boundary_status=0
fi
printf '[boundary exit %d]\n' "$boundary_status"

echo "Untrusted run claims:"
run sed -n 1,200p /candidate/run-input.json
run sed -n 1,200p /candidate/metrics.json
run sed -n 1,200p /candidate/codex-last.txt
run tail -n 25 /candidate/codex-output.log

echo "Structured trace summary:"
run python3 - /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-02-27-019f897d-bee6-7c43-8d06-4b42453460d7.jsonl <<'PY'
import collections
import json
import sys

path = sys.argv[1]
top = collections.Counter()
payload = collections.Counter()
commands = []
finals = []
parse_errors = 0
with open(path, encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        try:
            record = json.loads(line)
        except Exception:
            parse_errors += 1
            continue
        top[record.get("type", "<missing>")] += 1
        body = record.get("payload")
        if isinstance(body, dict):
            payload[body.get("type", "<missing>")] += 1
            if body.get("type") in {"function_call", "custom_tool_call"}:
                commands.append((line_number, body.get("name"), body.get("arguments") or body.get("input")))
            if body.get("type") == "message" and body.get("role") == "assistant":
                text = " ".join(
                    item.get("text", "")
                    for item in body.get("content", [])
                    if isinstance(item, dict)
                )
                if "RESULT:" in text or "KPROVE_PASSED" in text:
                    finals.append((line_number, text))
print("top-level types:", dict(sorted(top.items())))
print("payload types:", dict(sorted(payload.items())))
print("parse_errors:", parse_errors)
print("tool calls:", len(commands))
for item in commands:
    print(item)
print("final result-bearing messages:", finals)
PY

exit "$boundary_status"
