#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
status=0

echo '$ test ! -e /reference/reference-semantics'
test ! -e "$reference/reference-semantics"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

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

echo '$ test each required candidate artifact is a regular, non-symlink file'
for name in "${required[@]}"; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    printf 'OK regular non-symlink %s\n' "$name"
  else
    printf 'BAD missing/mistyped/symlinked %s\n' "$name"
    status=1
  fi
done

echo '$ find /candidate -maxdepth 1 -mindepth 1 -printf "%y %f -> %l\n" | sort'
find "$candidate" -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n' | sort

echo '$ cmp -s /reference/prompt.py /candidate/prompt.py'
cmp -s "$reference/prompt.py" "$candidate/prompt.py"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ cmp -s /reference/py2mpy.py /candidate/py2mpy.py'
cmp -s "$reference/py2mpy.py" "$candidate/py2mpy.py"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ sha256sum trusted and candidate provenance artifacts'
sha256sum \
  "$reference/prompt.py" "$candidate/prompt.py" \
  "$reference/py2mpy.py" "$candidate/py2mpy.py" \
  "$reference/canonical.py" \
  "$candidate/solution.py" "$candidate/solution.mpy" \
  "$candidate/semantic.k" "$candidate/verification.k" "$candidate/spec.k"

echo '$ validate run-input.json hashes and identity fields against trusted mounts'
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

data = json.loads(Path("/candidate/run-input.json").read_text())
checks = {
    "problem_id": data.get("problem_id") == "63-fibfib",
    "condition_name": data.get("condition", {}).get("name") == "bare",
    "problem_prompt_sha256": data.get("inputs", {}).get("problem_prompt_sha256")
        == hashlib.sha256(Path("/reference/prompt.py").read_bytes()).hexdigest(),
    "translator_sha256": data.get("inputs", {}).get("translator_sha256")
        == hashlib.sha256(Path("/reference/py2mpy.py").read_bytes()).hexdigest(),
}
for key, value in checks.items():
    print(f"{key}={value}")
if not all(checks.values()):
    raise SystemExit(1)
PY
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ validate every structured trace line is JSON and count record kinds'
python3 - <<'PY'
import collections
import glob
import json

paths = glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True)
print(f"trace_files={len(paths)}")
if len(paths) != 1:
    raise SystemExit(1)
outer = collections.Counter()
payload = collections.Counter()
lines = 0
for path in paths:
    with open(path, encoding="utf-8") as stream:
        for raw in stream:
            obj = json.loads(raw)
            lines += 1
            outer[obj.get("type")] += 1
            body = obj.get("payload")
            if isinstance(body, dict):
                payload[body.get("type")] += 1
print(f"lines={lines}")
print(f"outer_types={dict(outer)}")
print(f"payload_types={dict(payload)}")
PY
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ inspect untrusted codex-last/output generation claims (bounded grep)'
rg -n -m 120 \
  'KPROVE_PASSED|#Top|kprove|kompile|krun|prove\.sh|semantic\.k|verification\.k|spec\.k' \
  "$candidate/codex-last.txt" "$candidate/codex-output.log" \
  | tail -n 120
rc=${PIPESTATUS[0]}
echo "rg_exit=$rc"

echo '$ inspect bounded structured-trace claims'
python3 - <<'PY'
import glob
import json

for path in glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True):
    with open(path, encoding="utf-8") as stream:
        for number, raw in enumerate(stream, 1):
            obj = json.loads(raw)
            body = obj.get("payload")
            if not isinstance(body, dict):
                continue
            kind = body.get("type")
            text = None
            if kind in {"agent_message", "task_complete"}:
                text = body.get("message") or body.get("last_agent_message")
            elif kind == "custom_tool_call":
                name = body.get("name")
                call_input = body.get("input", "")
                if any(word in call_input for word in ("kprove", "kompile", "krun")):
                    text = f"tool={name} input={call_input}"
            if text:
                compact = " ".join(str(text).split())
                print(f"line={number} type={kind} claim={compact[:600]!r}")
PY
rc=$?
echo "trace_claim_extract_exit=$rc"
(( rc == 0 )) || status=1

echo "overall_exit=$status"
exit "$status"
