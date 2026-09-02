#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference
trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-19-57-019f8956-d570-7de0-a138-4dd2aa99331a.jsonl

printf 'Generated-semantics boundary\n'
if [[ ! -e "$reference/reference-semantics" ]]; then
  printf 'PASS: /reference/reference-semantics is absent\n'
else
  printf 'FAIL: /reference/reference-semantics exists\n'
fi

printf '\nRequired artifact types\n'
for path in \
  "$candidate/run-input.json" \
  "$candidate/metrics.json" \
  "$candidate/codex-last.txt" \
  "$candidate/codex-output.log" \
  "$trace" \
  "$candidate/prompt.py" \
  "$candidate/py2mpy.py" \
  "$candidate/solution.py" \
  "$candidate/solution.mpy" \
  "$candidate/semantic.k" \
  "$candidate/verification.k" \
  "$candidate/spec.k" \
  "$candidate/prove.sh"
do
  if [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
  elif [[ -f "$path" ]]; then
    printf 'REGULAR %s\n' "$path"
  elif [[ -e "$path" ]]; then
    printf 'MISTYPED %s\n' "$path"
  else
    printf 'MISSING %s\n' "$path"
  fi
done

printf '\nTrusted identity checks\n'
cmp "$candidate/prompt.py" "$reference/prompt.py"
printf 'prompt_cmp=%d\n' "$?"
cmp "$candidate/py2mpy.py" "$reference/py2mpy.py"
printf 'translator_cmp=%d\n' "$?"
sha256sum \
  "$candidate/prompt.py" "$reference/prompt.py" \
  "$candidate/py2mpy.py" "$reference/py2mpy.py" \
  "$candidate/solution.py" "$candidate/solution.mpy" \
  "$candidate/semantic.k" "$candidate/verification.k" "$candidate/spec.k"

printf '\nUntrusted metadata (parsed, not accepted)\n'
python3 -m json.tool "$candidate/run-input.json"
python3 -m json.tool "$candidate/metrics.json"
sed -n '1,200p' "$candidate/codex-last.txt"

printf '\nUntrusted log sizes and claim-bearing lines\n'
wc -l -c "$candidate/codex-output.log" "$trace"
rg -n -i -m 80 \
  'kprove|#Top|krun|random|differential|cmp|RESULT:|exit(ed| code| status)?' \
  "$candidate/codex-output.log" || true

printf '\nStructured-trace record types\n'
python3 - "$trace" <<'PY'
import collections
import json
import sys

counts = collections.Counter()
tool_calls = collections.Counter()
final_messages = []
with open(sys.argv[1], encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        counts[record.get("type", "<missing>")] += 1
        payload = record.get("payload", {})
        if payload.get("type") in {"custom_tool_call", "function_call"}:
            tool_calls[payload.get("name", "<missing>")] += 1
        if (
            record.get("type") == "event_msg"
            and payload.get("type") == "agent_message"
            and payload.get("phase") == "final_answer"
        ):
            final_messages.append((line_number, payload.get("message", "")))
print("record_counts", dict(sorted(counts.items())))
print("tool_call_counts", dict(sorted(tool_calls.items())))
for line_number, message in final_messages:
    print(f"final_message_line={line_number}")
    print(message)
PY

printf '\nCandidate-built artifacts ignored during reconstruction\n'
find "$candidate" -maxdepth 2 \
  \( -name '*-kompiled' -o -name '__pycache__' -o -name '*.pyc' \) \
  -printf '%y %p -> %l\n' | sort
