#!/usr/bin/env bash
set -u

check_regular() {
  local path=$1
  if [[ -f "$path" && ! -L "$path" && -r "$path" ]]; then
    printf 'REGULAR_READABLE %s\n' "$path"
  else
    printf 'BAD_REQUIRED_FILE %s\n' "$path"
    return 1
  fi
}

status=0
required_files=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/runtime-metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T00-40-28-019f97ca-0a3f-7213-9bc9-248130ea5052.jsonl
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
  /candidate/PROOF.md
)

for path in "${required_files[@]}"; do
  check_regular "$path" || status=1
done

for path in /candidate /reference/reference-semantics \
            /candidate/reference-semantics /generation-evidence/codex-trace; do
  if [[ -d "$path" && ! -L "$path" && -r "$path" ]]; then
    printf 'REAL_READABLE_DIRECTORY %s\n' "$path"
  else
    printf 'BAD_REQUIRED_DIRECTORY %s\n' "$path"
    status=1
  fi
done

printf '\nRECORDED FILE HASHES\n'
sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T00-40-28-019f97ca-0a3f-7213-9bc9-248130ea5052.jsonl

printf '\nLAUNCHER TREE HASHES\n'
PYTHONPATH=/opt/humaneval/tools python3 - <<'PY'
from pathlib import Path
from pipeline_contract import sha256_tree

for path in (
    "/reference/reference-semantics",
    "/candidate/reference-semantics",
    "/generation-evidence/codex-trace",
    "/candidate",
):
    print(sha256_tree(Path(path)), path)
PY

printf '\nCAMPAIGN LOCK EQUALITY\n'
python3 - <<'PY'
import json

with open("/audit-input.json", encoding="utf-8") as stream:
    audit_input = json.load(stream)
with open("/audit-campaign-lock.json", encoding="utf-8") as stream:
    lock = json.load(stream)
print(audit_input["audit_campaign"] == lock)
if audit_input["audit_campaign"] != lock:
    raise SystemExit(1)
PY
if [[ $? -ne 0 ]]; then status=1; fi

printf '\nSUPPLIED SEMANTICS SYMLINKS\n'
symlinks=$(
  find /reference/reference-semantics /candidate/reference-semantics \
    -type l -printf '%p -> %l\n'
)
if [[ -n "$symlinks" ]]; then
  printf '%s\n' "$symlinks"
  status=1
else
  printf 'NONE\n'
fi

printf '\nSUPPLIED SEMANTICS RECURSIVE DIFF\n'
diff -qr --no-dereference \
  /reference/reference-semantics /candidate/reference-semantics
diff_status=$?
printf 'DIFF_STATUS: %d\n' "$diff_status"
if [[ $diff_status -ne 0 ]]; then status=1; fi

printf '\nPROMPT AND TRANSLATOR COMPARISONS\n'
cmp /reference/prompt.py /candidate/prompt.py
prompt_status=$?
printf 'PROMPT_CMP_STATUS: %d\n' "$prompt_status"
if [[ $prompt_status -ne 0 ]]; then status=1; fi
cmp /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
printf 'TRANSLATOR_CMP_STATUS: %d\n' "$translator_status"
if [[ $translator_status -ne 0 ]]; then status=1; fi

printf '\nTRACE JSONL VALIDATION\n'
python3 - <<'PY'
import collections
import json

path = (
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T00-40-28-019f97ca-0a3f-7213-9bc9-248130ea5052.jsonl"
)
counts = collections.Counter()
line_count = 0
with open(path, encoding="utf-8") as stream:
    for line_count, line in enumerate(stream, 1):
        event = json.loads(line)
        counts[event.get("type")] += 1
print("JSON_LINES", line_count)
for key, value in sorted(counts.items()):
    print("EVENT_TYPE", key, value)
PY
if [[ $? -ne 0 ]]; then status=1; fi

printf '\nFINAL_STATUS: %d\n' "$status"
exit "$status"
