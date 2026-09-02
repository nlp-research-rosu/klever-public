#!/usr/bin/env bash
set -u

status=0

check_regular() {
  path="$1"
  if [[ -f "$path" && ! -L "$path" && -r "$path" ]]; then
    printf 'OK regular readable: %s\n' "$path"
  else
    printf 'FAIL required regular readable artifact: %s\n' "$path"
    status=1
  fi
}

check_directory() {
  path="$1"
  if [[ -d "$path" && ! -L "$path" && -r "$path" && -x "$path" ]]; then
    printf 'OK directory readable: %s\n' "$path"
  else
    printf 'FAIL required readable directory: %s\n' "$path"
    status=1
  fi
}

printf 'COMMAND: bash /audit-output/evidence/01_integrity.sh\n'
printf 'STAGE: required launcher and pipeline-v3 records\n'
for path in \
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
  /reference/py2mpy.py; do
  check_regular "$path"
done
check_directory /candidate
check_directory /reference/reference-semantics
check_directory /generation-evidence/codex-trace

printf 'STAGE: launcher metadata consistency and recorded file hashes\n'
python3 - <<'PY'
import hashlib
import json
import pathlib
import sys

audit = json.loads(pathlib.Path("/audit-input.json").read_text())
lock = json.loads(pathlib.Path("/audit-campaign-lock.json").read_text())
checks = []

def record(name, actual, expected):
    ok = actual == expected
    checks.append(ok)
    print(f"{'OK' if ok else 'FAIL'} {name}: actual={actual!r} expected={expected!r}")

record("record_layout", audit.get("record_layout"), "pipeline-v3")
record("semantics_mode", audit.get("semantics_mode"), "SUPPLIED_SEMANTICS")
record("condition", audit.get("condition"), "semantics")
record("audit_campaign_lock block", lock, audit.get("audit_campaign"))

hash_paths = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_runtime_metrics_sha256": "/generation-evidence/runtime-metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
}
for key, raw_path in hash_paths.items():
    path = pathlib.Path(raw_path)
    if not path.is_file() or path.is_symlink():
        print(f"FAIL {key}: missing, unreadable, or symlinked {path}")
        checks.append(False)
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    record(key, digest, audit["hashes"][key])

record(
    "campaign hash field",
    hashlib.sha256(pathlib.Path("/audit-campaign-lock.json").read_bytes()).hexdigest(),
    audit["hashes"]["audit_campaign_lock_sha256"],
)
record("manifest problem id", audit["manifest"]["problem_id"], "136-largest-smallest-integers")
record("task problem id", json.loads(pathlib.Path("/task.json").read_text())["problem_id"], audit["problem_id"])
record("run id", json.loads(pathlib.Path("/run.json").read_text())["run_id"], audit["run_id"])

trace_root = pathlib.Path("/generation-evidence/codex-trace")
trace_files = sorted(p for p in trace_root.rglob("*") if p.is_file())
record("structured trace file count", len(trace_files), 1)
if trace_files:
    rel = trace_files[0].relative_to(trace_root).as_posix()
    digest = hashlib.sha256(trace_files[0].read_bytes()).hexdigest()
    expected = json.loads(pathlib.Path("/generation-result.json").read_text())["outputs"]["evidence"].get(
        f"codex-trace/{rel}"
    )
    record(f"trace file {rel}", digest, expected)
    valid = True
    count = 0
    for count, line in enumerate(trace_files[0].read_text().splitlines(), 1):
        try:
            json.loads(line)
        except Exception as err:
            print(f"FAIL trace JSONL line {count}: {err}")
            valid = False
            break
    record("structured trace JSONL validity", valid, True)
    print(f"INFO structured trace lines={count}")

sys.exit(0 if all(checks) else 1)
PY
python_status=$?
if [[ "$python_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: no linked or unsupported entries in protected trees\n'
linked_or_special=0
while IFS= read -r entry; do
  printf 'FAIL linked or unsupported entry: %s\n' "$entry"
  linked_or_special=1
done < <(find /candidate/reference-semantics /reference/reference-semantics /generation-evidence/codex-trace \
  \( -type l -o \( ! -type f ! -type d \) \) -print)
if [[ "$linked_or_special" -eq 0 ]]; then
  printf 'OK no linked or unsupported entries\n'
else
  status=1
fi

printf 'STAGE: supplied-semantics recursive identity\n'
diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
diff_status=$?
printf 'EXIT diff semantics: %d\n' "$diff_status"
if [[ "$diff_status" -ne 0 ]]; then
  status=1
fi

cmp /reference/prompt.py /candidate/prompt.py
prompt_status=$?
printf 'EXIT cmp prompt: %d\n' "$prompt_status"
if [[ "$prompt_status" -ne 0 ]]; then
  status=1
fi

cmp /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
printf 'EXIT cmp translator: %d\n' "$translator_status"
if [[ "$translator_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: independent mounted-input SHA-256 manifest\n'
{
  find /candidate -maxdepth 1 -type f -print0
  find /candidate/reference-semantics /reference /generation-evidence -type f -print0
} \
  | sort -z \
  | xargs -0 sha256sum
printf 'INFO candidate-built caches intentionally excluded from source manifest:\n'
find /candidate -mindepth 1 -maxdepth 1 -type d \
  ! -name reference-semantics -printf '%f\n' | sort

printf 'FINAL EXIT: %d\n' "$status"
exit "$status"
