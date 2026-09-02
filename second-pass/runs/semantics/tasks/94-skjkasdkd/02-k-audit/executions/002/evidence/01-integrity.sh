#!/usr/bin/env bash
set -u

status=0
required_files=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /candidate/prompt.py
  /candidate/py2mpy.py
)

echo "COMMAND: stat required files and required directories"
for path in "${required_files[@]}" /candidate /generation-evidence/codex-trace \
  /reference/reference-semantics /candidate/reference-semantics; do
  if ! stat -c '%F %a %s %n' "$path"; then
    status=1
  fi
done

echo "COMMAND: check optional usage.json when present"
if [[ -e /generation-evidence/usage.json ]]; then
  stat -c '%F %a %s %n' /generation-evidence/usage.json || status=1
else
  echo "usage.json absent"
fi

echo "COMMAND: reject links or unsupported nodes in mounted input trees"
unsupported="$(
  find /candidate /reference/reference-semantics /generation-evidence \
    \( -type l -o \( ! -type f -a ! -type d \) \) -print
)"
if [[ -n "$unsupported" ]]; then
  echo "$unsupported"
  status=1
else
  echo "no linked or unsupported entries"
fi

echo "COMMAND: sha256sum launcher-declared regular inputs"
sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T03-15-21-019f8e0b-1e90-7332-9ade-efecd511ca1c.jsonl \
  /generation-evidence/usage.json || status=1

echo "COMMAND: compare campaign lock to audit-input audit_campaign"
python3 -c '
import json
from pathlib import Path
a = json.loads(Path("/audit-input.json").read_text())
l = json.loads(Path("/audit-campaign-lock.json").read_text())
assert a["audit_campaign"] == l, (a["audit_campaign"], l)
print("campaign objects identical")
' || status=1

echo "COMMAND: compare candidate prompt and translator byte-for-byte"
cmp /candidate/prompt.py /reference/prompt.py || status=1
cmp /candidate/py2mpy.py /reference/py2mpy.py || status=1

echo "COMMAND: recursively compare supplied semantics byte-for-byte"
diff -r --no-dereference /reference/reference-semantics \
  /candidate/reference-semantics || status=1

echo "COMMAND: independently hash every candidate regular file"
find /candidate -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum

echo "COMMAND: independently compute pipeline tree digests"
PYTHONPATH=/opt/humaneval/tools python3 -c '
from pathlib import Path
from pipeline_contract import sha256_tree
for p in (
    "/candidate",
    "/candidate/reference-semantics",
    "/reference/reference-semantics",
    "/generation-evidence/codex-trace",
):
    print(sha256_tree(Path(p)), p)
' || status=1

echo "FINAL_STATUS=$status"
exit "$status"
