#!/usr/bin/env bash
set +e

run() {
  printf 'COMMAND: %s\n' "$*"
  "$@"
  local status=$?
  printf 'EXIT STATUS: %s\n' "$status"
}

run sha256sum \
  /audit-input.json \
  /audit-campaign-lock.json \
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
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

run python3 -c 'import json, pathlib; a=json.loads(pathlib.Path("/audit-input.json").read_text()); b=json.loads(pathlib.Path("/audit-campaign-lock.json").read_text()); print("campaign_lock_matches_audit_block:", a["audit_campaign"] == b); raise SystemExit(0 if a["audit_campaign"] == b else 1)'

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py

run find /candidate/reference-semantics /reference/reference-semantics -type l -print
run diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics

printf 'COMMAND: compare typed entry manifests and SHA-256 values for candidate and trusted semantics trees\n'
python3 - <<'PY'
from hashlib import sha256
from pathlib import Path

def manifest(root_name):
    root = Path(root_name)
    rows = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            rows.append(("l", rel, path.readlink().as_posix()))
        elif path.is_dir():
            rows.append(("d", rel, ""))
        elif path.is_file():
            rows.append(("f", rel, sha256(path.read_bytes()).hexdigest()))
        else:
            rows.append(("?", rel, ""))
    return rows

candidate = manifest("/candidate/reference-semantics")
trusted = manifest("/reference/reference-semantics")
print("typed_manifests_equal:", candidate == trusted)
print("entry_count:", len(candidate))
for label, rows in (("candidate", candidate), ("trusted", trusted)):
    payload = "".join("\t".join(row) + "\n" for row in rows).encode()
    print(label + "_typed_manifest_sha256:", sha256(payload).hexdigest())
raise SystemExit(0 if candidate == trusted else 1)
PY
status=$?
printf 'EXIT STATUS: %s\n' "$status"

printf 'COMMAND: verify required pipeline-v3 records are regular, readable, and not symlinks\n'
python3 - <<'PY'
from pathlib import Path

required = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/runtime-metrics.json",
    "/generation-evidence/usage.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
]
ok = True
for item in required:
    path = Path(item)
    good = path.exists() and path.is_file() and not path.is_symlink()
    readable = False
    if good:
        try:
            path.open("rb").read(1)
            readable = True
        except OSError:
            pass
    print(f"{item}: regular_non_symlink={good} readable={readable}")
    ok &= good and readable
trace = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace.rglob("*")) if trace.exists() else []
trace_ok = trace.is_dir() and not trace.is_symlink() and any(p.is_file() and not p.is_symlink() for p in trace_files)
print(f"{trace}: directory_non_symlink={trace.is_dir() and not trace.is_symlink()} has_regular_trace={trace_ok}")
ok &= trace_ok
raise SystemExit(0 if ok else 1)
PY
status=$?
printf 'EXIT STATUS: %s\n' "$status"

printf 'COMMAND: verify required candidate proof artifacts are regular, readable, and not symlinks\n'
python3 - <<'PY'
from pathlib import Path

required = [
    "/candidate/solution.py",
    "/candidate/solution.mpy",
    "/candidate/verification.k",
    "/candidate/spec.k",
    "/candidate/prove.sh",
    "/candidate/PROOF.md",
]
ok = True
for item in required:
    path = Path(item)
    good = path.exists() and path.is_file() and not path.is_symlink()
    readable = False
    if good:
        try:
            path.open("rb").read(1)
            readable = True
        except OSError:
            pass
    print(f"{item}: regular_non_symlink={good} readable={readable}")
    ok &= good and readable
raise SystemExit(0 if ok else 1)
PY
status=$?
printf 'EXIT STATUS: %s\n' "$status"

printf 'COMMAND: independently validate all JSON and JSONL generation records\n'
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path

json_paths = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
]
for path in json_paths:
    json.loads(path.read_text())
    print(f"{path}: valid JSON")

for path in sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl")):
    counts = Counter()
    total = 0
    for line_number, line in enumerate(path.open(), 1):
        obj = json.loads(line)
        counts[str(obj.get("type", "<missing>"))] += 1
        total = line_number
    print(f"{path}: valid JSONL lines={total} event_types={dict(sorted(counts.items()))}")
PY
status=$?
printf 'EXIT STATUS: %s\n' "$status"
