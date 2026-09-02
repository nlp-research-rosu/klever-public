#!/usr/bin/env bash
set -u

required=(
  /audit-input.json
  /run.json
  /task.json
  /generation-result.json
  /generation/invocation.json
  /generation/metrics.json
  /generation/runtime-metrics.json
  /generation/usage.json
  /generation/codex-last.txt
  /generation/codex-output.log
  /generation/prompt.txt
  /generation/codex-trace
  /candidate
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
)

for path in "${required[@]}"; do
  stat -c '%F | %A | %s | %n' "$path"
  printf 'STAT_EXIT %s %s\n' "$?" "$path"
done

sha256sum \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation/invocation.json \
  /generation/metrics.json \
  /generation/runtime-metrics.json \
  /generation/usage.json \
  /generation/codex-last.txt \
  /generation/codex-output.log \
  /generation/prompt.txt \
  /generation/codex-trace/2026/07/24/rollout-2026-07-24T22-25-55-019f974e-dac3-7be2-961b-a3bf7b11aa27.jsonl

cmp -s /candidate/prompt.py /reference/prompt.py
printf 'PROMPT_CMP_EXIT %s\n' "$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'TRANSLATOR_CMP_EXIT %s\n' "$?"
diff -qr --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics
printf 'REFERENCE_SEMANTICS_DIFF_EXIT %s\n' "$?"

printf 'CANDIDATE_SYMLINKS '
find /candidate -type l -print | wc -l
printf 'CANDIDATE_REFSEM_SYMLINKS '
find /candidate/reference-semantics -type l -print | wc -l
printf 'TRUSTED_REFSEM_SYMLINKS '
find /reference/reference-semantics -type l -print | wc -l
printf 'GENERATION_TRACE_SYMLINKS '
find /generation/codex-trace -type l -print | wc -l

python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path

trace = Path("/generation/codex-trace/2026/07/24/rollout-2026-07-24T22-25-55-019f974e-dac3-7be2-961b-a3bf7b11aa27.jsonl")
top = Counter()
payload = Counter()
lines = 0
for lines, raw in enumerate(trace.open(encoding="utf-8"), 1):
    obj = json.loads(raw)
    top[obj.get("type")] += 1
    body = obj.get("payload")
    if isinstance(body, dict):
        payload[body.get("type")] += 1
print("TRACE_JSON_LINES", lines)
print("TRACE_TOP_TYPES", dict(sorted(top.items(), key=lambda kv: str(kv[0]))))
print("TRACE_PAYLOAD_TYPES", dict(sorted(payload.items(), key=lambda kv: str(kv[0]))))
PY
printf 'TRACE_JSON_PARSE_EXIT %s\n' "$?"

