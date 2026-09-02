#!/usr/bin/env bash
set -u

status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
}

required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T07-18-13-019f8ee9-77c1-73c2-84ab-883b53530ad9.jsonl
  /reference/prompt.py
  /reference/canonical.py
  /reference/py2mpy.py
  /reference/reference-semantics/semantics.k
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/spec.k
  /candidate/verification.k
  /candidate/prove.sh
  /candidate/reference-semantics/semantics.k
)

printf '$ test -r <each required legacy-selected-stage1 and proof artifact>\n'
for path in "${required[@]}"; do
  if [[ ! -r "$path" ]]; then
    printf 'UNREADABLE %s\n' "$path"
    status=1
  fi
done
printf '[exit %d]\n' "$status"

run sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T07-18-13-019f8ee9-77c1-73c2-84ab-883b53530ad9.jsonl \
  /reference/prompt.py \
  /reference/canonical.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics

printf '$ find /candidate/reference-semantics /reference/reference-semantics -type l\n'
symlinks=$(find /candidate/reference-semantics /reference/reference-semantics -type l -print)
if [[ -n "$symlinks" ]]; then
  printf '%s\n' "$symlinks"
  status=1
fi
printf '[exit %d; symlinks=%s]\n' "$([[ -z "$symlinks" ]] && printf 0 || printf 1)" "$([[ -z "$symlinks" ]] && printf 0 || printf 1)"

printf '$ compare recursive path/type/link inventories\n'
candidate_inventory=$(mktemp)
reference_inventory=$(mktemp)
find /candidate/reference-semantics -printf '%P\t%y\t%l\n' | sort > "$candidate_inventory"
find /reference/reference-semantics -printf '%P\t%y\t%l\n' | sort > "$reference_inventory"
diff -u "$reference_inventory" "$candidate_inventory"
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then
  status=1
fi

printf '$ compare audit_campaign object with campaign lock and recorded lock hash\n'
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit_path = Path("/audit-input.json")
lock_path = Path("/audit-campaign-lock.json")
audit = json.loads(audit_path.read_text())
lock_bytes = lock_path.read_bytes()
lock = json.loads(lock_bytes)
actual_hash = hashlib.sha256(lock_bytes).hexdigest()
recorded_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"object_equal={audit['audit_campaign'] == lock}")
print(f"actual_sha256={actual_hash}")
print(f"recorded_sha256={recorded_hash}")
if audit["audit_campaign"] != lock or actual_hash != recorded_hash:
    raise SystemExit(1)
PY
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then
  status=1
fi

printf '$ independently hash every supplied-semantics file by relative path\n'
(cd /reference/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum)
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then
  status=1
fi

printf '$ independently hash every candidate supplied-semantics file by relative path\n'
(cd /candidate/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum)
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then
  status=1
fi

printf 'FINAL_STATUS=%d\n' "$status"
exit "$status"
