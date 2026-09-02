#!/usr/bin/env bash
set -uo pipefail

failures=0

check_status() {
  local label="$1"
  shift
  printf 'COMMAND[%s]:' "$label"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT[%s]=%d\n' "$label" "$status"
  if (( status != 0 )); then
    failures=$((failures + 1))
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
  /generation-evidence/runtime-metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
  /candidate/PROOF.md
)

printf 'record_layout=%s\n' "$(
  python3 -c 'import json; print(json.load(open("/audit-input.json"))["record_layout"])'
)"
printf 'semantics_mode=%s\n' "$(
  python3 -c 'import json; print(json.load(open("/audit-input.json"))["semantics_mode"])'
)"
for path in "${required[@]}"; do
  if [[ -f "$path" && -r "$path" && ! -L "$path" ]]; then
    printf 'REQUIRED_OK %s\n' "$path"
  else
    printf 'REQUIRED_BAD %s\n' "$path"
    failures=$((failures + 1))
  fi
done

check_status campaign-json-equality python3 -c \
  'import json; assert json.load(open("/audit-input.json"))["audit_campaign"] == json.load(open("/audit-campaign-lock.json"))'
check_status task-json-consistency python3 -c \
  'import json; outer=json.load(open("/audit-input.json"))["manifest"]; task=json.load(open("/task.json")); assert all(outer.get(key) == value for key, value in task.items())'
check_status prompt-byte-identity cmp -s /candidate/prompt.py /reference/prompt.py
check_status translator-byte-identity cmp -s /candidate/py2mpy.py /reference/py2mpy.py
check_status supplied-semantics-byte-tree diff -r --no-dereference \
  /reference/reference-semantics /candidate/reference-semantics

printf 'SYMLINK_SCAN candidate/reference-semantics and trusted tree\n'
find /candidate/reference-semantics /reference/reference-semantics -type l \
  -printf 'SYMLINK %p -> %l\n'
symlink_count="$(find /candidate/reference-semantics /reference/reference-semantics \
  -type l -printf x | wc -c)"
printf 'symlink_count=%s\n' "$symlink_count"
if (( symlink_count != 0 )); then
  failures=$((failures + 1))
fi

printf 'REFERENCE_SEMANTICS_MANIFEST candidate\n'
(
  cd /candidate/reference-semantics
  find . -mindepth 1 -printf '%y %P\n' | LC_ALL=C sort
  find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
)
printf 'REFERENCE_SEMANTICS_MANIFEST trusted\n'
(
  cd /reference/reference-semantics
  find . -mindepth 1 -printf '%y %P\n' | LC_ALL=C sort
  find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
)

trace=/generation-evidence/codex-trace/2026/07/29/rollout-2026-07-29T07-22-04-019fadd3-27b0-7ad3-ba1b-0db75f23c44f.jsonl
check_status trace-regular-readable bash -c \
  '[[ -f "$1" && -r "$1" && ! -L "$1" ]]' _ "$trace"
check_status trace-jsonl-parse python3 -c \
  'import json,sys; [json.loads(line) for line in open(sys.argv[1])]' "$trace"
printf 'trace_lines=%s\n' "$(wc -l < "$trace")"

printf 'DECLARED_AND_ACTUAL_HASHES\n'
while IFS=$'\t' read -r key expected path; do
  actual="$(sha256sum "$path" | awk '{print $1}')"
  printf '%s expected=%s actual=%s path=%s\n' "$key" "$expected" "$actual" "$path"
  if [[ "$expected" != "$actual" ]]; then
    failures=$((failures + 1))
  fi
done < <(python3 - <<'PY'
import json

record = json.load(open("/audit-input.json"))
hashes = record["hashes"]
items = [
    ("audit_campaign_lock_sha256", "/audit-campaign-lock.json"),
    ("canonical_sha256", "/reference/canonical.py"),
    ("trusted_prompt_sha256", "/reference/prompt.py"),
    ("candidate_prompt_sha256", "/candidate/prompt.py"),
    ("trusted_translator_sha256", "/reference/py2mpy.py"),
    ("candidate_translator_sha256", "/candidate/py2mpy.py"),
    ("run_manifest_sha256", "/run.json"),
    ("task_manifest_sha256", "/task.json"),
    ("stage1_result_sha256", "/generation-result.json"),
    ("stage1_invocation_sha256", "/generation-evidence/invocation.json"),
    ("generation_metrics_sha256", "/generation-evidence/metrics.json"),
    ("generation_runtime_metrics_sha256", "/generation-evidence/runtime-metrics.json"),
    ("generation_usage_sha256", "/generation-evidence/usage.json"),
    ("generation_codex_last_sha256", "/generation-evidence/codex-last.txt"),
    ("generation_codex_output_sha256", "/generation-evidence/codex-output.log"),
    ("generation_prompt_sha256", "/generation-evidence/prompt.txt"),
]
for key, path in items:
    print(key, hashes[key], path, sep="\t")
PY
)

trace_expected="$(
  python3 -c '
import json
rel = "codex-trace/2026/07/29/rollout-2026-07-29T07-22-04-019fadd3-27b0-7ad3-ba1b-0db75f23c44f.jsonl"
print(json.load(open("/generation-result.json"))["outputs"]["evidence"][rel])
'
)"
trace_actual="$(sha256sum "$trace" | awk '{print $1}')"
printf 'trace_file expected=%s actual=%s path=%s\n' "$trace_expected" "$trace_actual" "$trace"
if [[ "$trace_expected" != "$trace_actual" ]]; then
  failures=$((failures + 1))
fi

printf 'integrity_failures=%d\n' "$failures"
exit "$failures"
