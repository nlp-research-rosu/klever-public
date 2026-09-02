#!/usr/bin/env bash
set -u

overall=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

printf 'Stage 1 provenance and integrity reconstruction\n'
printf 'Untrusted candidate metadata is summarized only as a claim.\n'

run stat -c '%F %a %U:%G %s %n -> %N' \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/prompt.py /candidate/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k \
  /candidate/spec.k /candidate/prove.sh

run sha256sum \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/prompt.py /candidate/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k \
  /candidate/spec.k /candidate/prove.sh \
  /reference/prompt.py /reference/canonical.py /reference/py2mpy.py

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py

printf '\n$ find /candidate -type l -printf ...\n'
find /candidate -type l -printf '%p -> %l\n'
status=$?
printf '[exit %d; empty output means no candidate symlinks]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '\n$ test ! -e /reference/reference-semantics\n'
if test ! -e /reference/reference-semantics; then
  printf 'GENERATED_SEMANTICS boundary satisfied: trusted reference-semantics is absent\n'
  printf '[exit 0]\n'
else
  printf 'GENERATED_SEMANTICS boundary breach: trusted reference-semantics exists\n'
  printf '[exit 1]\n'
  overall=1
fi

run sed -n '1,120p' /candidate/run-input.json
run sed -n '1,120p' /candidate/metrics.json
run sed -n '1,120p' /candidate/codex-last.txt

printf '\n$ rg -n selected-generation-claims /candidate/codex-output.log\n'
rg -n \
  'RESULT:|python property checks|kprove|#Top|semantic-kompiled|prove.sh' \
  /candidate/codex-output.log | tail -n 80
status=${PIPESTATUS[0]}
printf '[rg exit %d]\n' "$status"
if [ "$status" -gt 1 ]; then overall=1; fi

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-46-48-019f8938-7c69-74e0-acdd-659b3d9ac5e9.jsonl
run stat -c '%F %s %n' "$trace"
run sha256sum "$trace"

printf '\n$ python3 trace structural summary\n'
python3 - "$trace" <<'PY'
import collections
import json
import sys

path = sys.argv[1]
top = collections.Counter()
payload = collections.Counter()
commands = []
finals = []
with open(path, encoding="utf-8") as fh:
    for number, line in enumerate(fh, 1):
        item = json.loads(line)
        top[item.get("type")] += 1
        p = item.get("payload", {})
        if isinstance(p, dict):
            payload[p.get("type")] += 1
            if p.get("type") in {"custom_tool_call", "function_call"}:
                commands.append((number, p.get("name"), p.get("input") or p.get("arguments")))
            if p.get("type") == "agent_message" and p.get("phase") == "final_answer":
                finals.append((number, p.get("message")))
print("top-level types:", dict(sorted(top.items())))
print("payload types:", dict(sorted(payload.items(), key=lambda kv: str(kv[0]))))
print("tool/function call count:", len(commands))
print("last five calls:")
for row in commands[-5:]:
    print(row)
print("final claims:")
for row in finals:
    print(row)
PY
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

printf '\nOverall provenance script status: %d\n' "$overall"
exit "$overall"
