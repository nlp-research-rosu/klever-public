#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference

printf '%s\n' '=== rendered semantics boundary ==='
if [[ -e "$reference_root/reference-semantics" || -L "$reference_root/reference-semantics" ]]; then
  printf '%s\n' 'BREACH: /reference/reference-semantics exists'
  ls -ld "$reference_root/reference-semantics"
else
  printf '%s\n' 'OK: /reference/reference-semantics is absent'
fi

printf '%s\n' '=== required candidate artifact types ==='
required=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
  prove.sh
)
for rel in "${required[@]}"; do
  path="$candidate_root/$rel"
  if [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
  elif [[ -f "$path" ]]; then
    printf 'REGULAR %s\n' "$path"
  elif [[ -e "$path" ]]; then
    printf 'MISTYPED %s\n' "$path"
    stat -c 'mode=%F permissions=%A size=%s' "$path"
  else
    printf 'MISSING %s\n' "$path"
  fi
done

printf '%s\n' '=== structured traces ==='
find -P "$candidate_root/codex-trace" -type f -printf 'REGULAR %p\n' 2>/dev/null | sort
find -P "$candidate_root/codex-trace" -type l -printf 'SYMLINK %p -> %l\n' 2>/dev/null | sort

printf '%s\n' '=== prompt and translator byte comparisons ==='
cmp -s "$candidate_root/prompt.py" "$reference_root/prompt.py"
printf 'prompt_cmp_exit=%d\n' "$?"
cmp -s "$candidate_root/py2mpy.py" "$reference_root/py2mpy.py"
printf 'translator_cmp_exit=%d\n' "$?"
sha256sum \
  "$candidate_root/prompt.py" "$reference_root/prompt.py" \
  "$candidate_root/py2mpy.py" "$reference_root/py2mpy.py"

printf '%s\n' '=== all candidate entries (compiled products are inventory only) ==='
find -P "$candidate_root" -printf '%y %p -> %l\n' | sort

printf '%s\n' '=== untrusted run claims ==='
python3 -m json.tool --sort-keys "$candidate_root/run-input.json"
python3 -m json.tool --sort-keys "$candidate_root/metrics.json"
printf '%s\n' '-- codex-last.txt --'
sed -n '1,200p' "$candidate_root/codex-last.txt"
printf '%s\n' '-- codex-output claim markers --'
wc -lc "$candidate_root/codex-output.log"
rg -n \
  'RESULT:|#Top|krun multiply|Warning|Error|timed out|Script completed|exit_code' \
  "$candidate_root/codex-output.log" | tail -n 120

printf '%s\n' '=== structured trace record census and tool-call claims ==='
for trace in "$candidate_root"/codex-trace/*/*/*/*.jsonl; do
  [[ -f "$trace" ]] || continue
  printf 'TRACE %s\n' "$trace"
  wc -lc "$trace"
  python3 - "$trace" <<'PY'
import collections
import json
import re
import sys

path = sys.argv[1]
records = []
with open(path, encoding="utf-8") as handle:
    for line_number, line in enumerate(handle, 1):
        record = json.loads(line)
        records.append(record)

counts = collections.Counter(record.get("type", "") for record in records)
for name, count in sorted(counts.items()):
    print(f"{count:6d} {name}")

for record in records:
    if record.get("type") != "response_item":
        continue
    payload = record.get("payload", {})
    payload_type = payload.get("type", "")
    if payload_type not in {"custom_tool_call", "function_call", "message"}:
        continue
    if payload_type == "custom_tool_call":
        detail = payload.get("input", "")
    elif payload_type == "function_call":
        detail = payload.get("arguments", "")
    else:
        detail = json.dumps(payload.get("content", []), sort_keys=True)
    detail = re.sub(r"[\r\n]+", " ", detail)
    print("\t".join([
        payload_type,
        payload.get("name", ""),
        payload.get("call_id", ""),
        detail,
    ]))
PY
done
