#!/usr/bin/env bash
set -u

echo "== toolchain =="
for tool in kup kompile krun kprove kast; do
  resolved="$(command -v "$tool" 2>/dev/null || true)"
  printf '%s=%s\n' "$tool" "${resolved:-ABSENT}"
done
kompile --version
kprove --version

echo "== generated-semantics infrastructure boundary =="
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  echo "BREACH: /reference/reference-semantics exists"
  stat -c '%F %N' /reference/reference-semantics
  boundary_status=1
else
  echo "OK: /reference/reference-semantics is absent"
  boundary_status=0
fi

echo "== candidate inventory and types =="
find /candidate -printf '%y %M %p -> %l\n' | sort

echo "== trusted comparisons =="
cmp /candidate/prompt.py /reference/prompt.py
prompt_status=$?
printf 'prompt_cmp_exit=%d\n' "$prompt_status"
cmp /candidate/py2mpy.py /reference/py2mpy.py
translator_status=$?
printf 'translator_cmp_exit=%d\n' "$translator_status"

echo "== source hashes =="
sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k \
  /reference/canonical.py

echo "== provenance claims =="
for source in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log
do
  stat -c '%F %s bytes %N' "$source"
done
trace_path="$(find /candidate/codex-trace -type f -name '*.jsonl' -print -quit)"
stat -c '%F %s bytes %N' "$trace_path"
wc -l /candidate/codex-output.log "$trace_path"
python3 -m json.tool /candidate/run-input.json
python3 -m json.tool /candidate/metrics.json

echo "== structured trace event summary =="
python3 - "$trace_path" <<'PY'
import collections
import json
import sys

path = sys.argv[1]
outer = collections.Counter()
payload = collections.Counter()
tool_names = collections.Counter()
messages = []
with open(path, encoding="utf-8") as stream:
    for line_no, line in enumerate(stream, 1):
        item = json.loads(line)
        outer[item.get("type")] += 1
        body = item.get("payload") or {}
        payload[body.get("type")] += 1
        if body.get("type") == "custom_tool_call":
            tool_names[body.get("name")] += 1
        if body.get("type") in {"agent_message", "message"}:
            text = body.get("message")
            if text is None:
                parts = body.get("content") or []
                text = " ".join(p.get("text", "") for p in parts if isinstance(p, dict))
            if text:
                messages.append((line_no, body.get("type"), text[:240].replace("\n", " ")))
print("outer_types", dict(sorted(outer.items(), key=lambda x: str(x[0]))))
print("payload_types", dict(sorted(payload.items(), key=lambda x: str(x[0]))))
print("tool_names", dict(sorted(tool_names.items(), key=lambda x: str(x[0]))))
print("last_messages")
for row in messages[-8:]:
    print(row)
PY

exit $(( boundary_status || prompt_status || translator_status ))
