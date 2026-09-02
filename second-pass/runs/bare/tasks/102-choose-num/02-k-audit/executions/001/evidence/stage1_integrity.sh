#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/stage1-integrity.log
exec > >(tee "$LOG") 2>&1

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'STAGE 1 INPUT AND PROVENANCE INTEGRITY\n'
run kompile --version
run kprove --version
run python3 --version
run test ! -e /reference/reference-semantics
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
run cmp -s /candidate/solution.py /tmp/audit-work/solution.py
run cmp -s /candidate/solution.mpy /tmp/audit-work/solution.mpy
run cmp -s /candidate/semantic.k /tmp/audit-work/semantic.k
run cmp -s /candidate/verification.k /tmp/audit-work/verification.k
run cmp -s /candidate/spec.k /tmp/audit-work/spec.k

required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k
  spec.k prove.sh
)
integrity_status=0
for name in "${required[@]}"; do
  path="/candidate/$name"
  if [[ ! -e "$path" && ! -L "$path" ]]; then
    printf 'MISSING %s\n' "$path"
    integrity_status=1
  elif [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
    integrity_status=1
  elif [[ ! -f "$path" ]]; then
    printf 'MISTYPED %s type=%s\n' "$path" "$(stat -c %F "$path")"
    integrity_status=1
  else
    printf 'REGULAR %s bytes=%s\n' "$path" "$(stat -c %s "$path")"
  fi
done

printf 'candidate top-level entries (extras are visible here)\n'
run find /candidate -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n'
printf 'candidate symlinks at any depth\n'
run find /candidate -type l -printf '%p -> %l\n'

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-26-09-019f8993-71ba-7d00-b31b-ee49d225f2ae.jsonl
run python3 -c '
import collections
import json
import pathlib
import sys

p = pathlib.Path(sys.argv[1])
top = collections.Counter()
payload = collections.Counter()
commands = []
final_messages = []
for line_number, line in enumerate(p.open(encoding="utf-8"), 1):
    obj = json.loads(line)
    top[obj.get("type")] += 1
    item = obj.get("payload", {})
    payload[item.get("type", "none")] += 1
    if item.get("type") == "custom_tool_call":
        commands.append(item.get("name"))
    if item.get("type") == "message" and item.get("role") == "assistant":
        text = " ".join(part.get("text", "") for part in item.get("content", []))
        final_messages.append(text)
print(f"json_lines={sum(top.values())}")
print(f"top_types={dict(sorted(top.items()))}")
print(f"payload_types={dict(sorted(payload.items()))}")
print(f"tool_calls={len(commands)} names={commands}")
print("last_assistant_message=" + (final_messages[-1] if final_messages else "<none>"))
' "$trace"

printf 'untrusted metadata claims\n'
run sed -n 1,220p /candidate/run-input.json
run sed -n 1,220p /candidate/metrics.json
run sed -n 1,220p /candidate/codex-last.txt

printf 'integrity_status=%d\n' "$integrity_status"
exit "$integrity_status"
