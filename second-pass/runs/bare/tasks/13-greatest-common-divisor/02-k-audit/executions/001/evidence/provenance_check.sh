#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference
trace_file=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T04-01-45-019f890f-3e04-7d23-b491-4c26b5662f21.jsonl

status=0

printf '%s\n' 'MODE_BOUNDARY'
if [[ -e "$reference_root/reference-semantics" || -L "$reference_root/reference-semantics" ]]; then
  printf '%s\n' 'ERROR: reference-semantics exists in GENERATED_SEMANTICS mode'
  status=1
else
  printf '%s\n' 'OK: reference-semantics is absent (including no symlink)'
fi

printf '%s\n' 'REQUIRED_ARTIFACT_TYPES'
required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy semantic.k gcd-spec.k
  loop-spec.k loop-verification.k verification.k spec.k prove.sh
)
for name in "${required[@]}"; do
  path="$candidate_root/$name"
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'OK regular %s\n' "$path"
  else
    printf 'ERROR missing/mistyped/symlinked %s\n' "$path"
    status=1
  fi
done
if [[ -f "$trace_file" && ! -L "$trace_file" ]]; then
  printf 'OK regular %s\n' "$trace_file"
else
  printf 'ERROR missing/mistyped/symlinked %s\n' "$trace_file"
  status=1
fi

printf '%s\n' 'ALL_CANDIDATE_SYMLINKS'
find "$candidate_root" -type l -printf '%p -> %l\n' | sort

printf '%s\n' 'TOP_LEVEL_INVENTORY'
find "$candidate_root" -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort

printf '%s\n' 'TRUSTED_BYTE_COMPARISONS'
for name in prompt.py py2mpy.py; do
  if cmp -s "$candidate_root/$name" "$reference_root/$name"; then
    printf 'IDENTICAL %s\n' "$name"
  else
    printf 'CHANGED %s\n' "$name"
    status=1
  fi
done

printf '%s\n' 'METADATA_JSON_VALIDATION'
python3 -m json.tool "$candidate_root/run-input.json" >/dev/null
json_status=$?
printf 'run-input.json json_status=%d\n' "$json_status"
(( json_status == 0 )) || status=1
python3 -m json.tool "$candidate_root/metrics.json" >/dev/null
json_status=$?
printf 'metrics.json json_status=%d\n' "$json_status"
(( json_status == 0 )) || status=1

printf '%s\n' 'SHA256'
sha256sum \
  "$candidate_root/run-input.json" \
  "$candidate_root/metrics.json" \
  "$candidate_root/codex-last.txt" \
  "$candidate_root/codex-output.log" \
  "$trace_file" \
  "$candidate_root/prompt.py" \
  "$candidate_root/py2mpy.py" \
  "$candidate_root/solution.py" \
  "$candidate_root/solution.mpy" \
  "$candidate_root/semantic.k" \
  "$candidate_root/gcd-spec.k" \
  "$candidate_root/loop-spec.k" \
  "$candidate_root/loop-verification.k" \
  "$candidate_root/verification.k" \
  "$candidate_root/spec.k" \
  "$reference_root/canonical.py" \
  "$reference_root/prompt.py" \
  "$reference_root/py2mpy.py"

printf '%s\n' 'UNTRUSTED_CLAIM_FILES'
wc -l -c \
  "$candidate_root/run-input.json" \
  "$candidate_root/metrics.json" \
  "$candidate_root/codex-last.txt" \
  "$candidate_root/codex-output.log" \
  "$trace_file"
printf 'codex-output #Top mentions='
rg -c '#Top' "$candidate_root/codex-output.log" || true
printf 'codex-output WarnStuckClaimState mentions='
rg -c 'WarnStuckClaimState' "$candidate_root/codex-output.log" || true
printf 'trace #Top-bearing lines='
rg -c '#Top' "$trace_file" || true
printf 'trace WarnStuckClaimState-bearing lines='
rg -c 'WarnStuckClaimState' "$trace_file" || true

exit "$status"
