#!/usr/bin/env bash
set -uo pipefail

status=0

required=(
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
  /reference/reference-semantics
  /candidate
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/reference-semantics
)

echo "Required launcher/provenance records and mounts:"
for path in "${required[@]}"; do
  if [[ -r "$path" && ! -L "$path" ]]; then
    printf 'OK regular-or-directory, readable, non-symlink: %s\n' "$path"
  else
    printf 'FAIL absent, unreadable, or symlinked: %s\n' "$path"
    status=1
  fi
done

echo
echo "Optional historical usage record:"
if [[ -r /generation-evidence/usage.json && ! -L /generation-evidence/usage.json ]]; then
  echo "PRESENT regular readable non-symlink: /generation-evidence/usage.json"
else
  echo "ABSENT/INVALID: /generation-evidence/usage.json"
  status=1
fi

echo
echo "Unexpected symlinks in mounted trees:"
symlinks=$(find /candidate /reference/reference-semantics /generation-evidence/codex-trace -type l -print)
if [[ -n "$symlinks" ]]; then
  printf '%s\n' "$symlinks"
  status=1
else
  echo "none"
fi

echo
echo "Campaign lock structural equality and selected manifest fields:"
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock_path = Path("/audit-campaign-lock.json")
lock = json.loads(lock_path.read_text())
actual_lock_hash = hashlib.sha256(lock_path.read_bytes()).hexdigest()
checks = {
    "campaign_block_equals_lock": audit["audit_campaign"] == lock,
    "lock_hash_matches_recorded": actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"],
    "condition_is_semantics": audit["condition"] == "semantics",
    "semantics_mode_is_supplied": audit["semantics_mode"] == "SUPPLIED_SEMANTICS",
    "record_layout_is_legacy_selected_stage1": audit["record_layout"] == "legacy-selected-stage1",
    "problem_id_matches": audit["problem_id"] == "2-truncate-number",
}
for name, value in checks.items():
    print(f"{name}: {value}")
if not all(checks.values()):
    raise SystemExit(1)
PY
if (( $? != 0 )); then
  status=1
fi

echo
echo "Recorded-file SHA-256 checks:"
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
expected = audit["hashes"]
files = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
}
ok = True
for key, filename in files.items():
    actual = hashlib.sha256(Path(filename).read_bytes()).hexdigest()
    matched = actual == expected[key]
    print(f"{key}: {matched} actual={actual} expected={expected[key]}")
    ok &= matched
if not ok:
    raise SystemExit(1)
PY
if (( $? != 0 )); then
  status=1
fi

echo
echo "Trace file hashes declared by generation-result.json:"
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

result = json.loads(Path("/generation-result.json").read_text())
ok = True
for relpath, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relpath
    if not path.is_file() or path.is_symlink():
        print(f"FAIL missing/non-file/symlink: {path}")
        ok = False
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    matched = actual == expected
    print(f"{relpath}: {matched} actual={actual} expected={expected}")
    ok &= matched
if not ok:
    raise SystemExit(1)
PY
if (( $? != 0 )); then
  status=1
fi

echo
echo "Trusted/candidate exact-file comparisons:"
for pair in \
  "/reference/prompt.py /candidate/prompt.py" \
  "/reference/py2mpy.py /candidate/py2mpy.py"
do
  read -r trusted candidate <<<"$pair"
  if cmp -s "$trusted" "$candidate"; then
    echo "IDENTICAL: $trusted == $candidate"
  else
    echo "DIFFERENT: $trusted != $candidate"
    status=1
  fi
done

echo
echo "Supplied-semantics recursive type/path/content comparison:"
python3 - <<'PY'
import hashlib
import os
from pathlib import Path

def inventory(root_name):
    root = Path(root_name)
    out = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                out[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                out[rel] = ("dir", None)
            elif path.is_file():
                out[rel] = ("file", hashlib.sha256(path.read_bytes()).hexdigest())
            else:
                out[rel] = ("other", None)
    return out

trusted = inventory("/reference/reference-semantics")
candidate = inventory("/candidate/reference-semantics")
all_paths = sorted(set(trusted) | set(candidate))
ok = True
for rel in all_paths:
    if trusted.get(rel) != candidate.get(rel):
        ok = False
        print(f"DIFFERENCE {rel}: trusted={trusted.get(rel)} candidate={candidate.get(rel)}")
print(f"trusted_entries={len(trusted)} candidate_entries={len(candidate)} exact_match={ok}")
if not ok:
    raise SystemExit(1)
PY
if (( $? != 0 )); then
  status=1
fi

echo
echo "INTEGRITY_CHECK_EXIT=$status"
exit "$status"
