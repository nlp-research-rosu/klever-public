#!/usr/bin/env bash
set -uo pipefail

candidate_root=/candidate
reference_root=/reference

printf 'GENERATED_SEMANTICS boundary\n'
if [[ -e "$reference_root/reference-semantics" || -L "$reference_root/reference-semantics" ]]; then
  printf 'BREACH: %s exists\n' "$reference_root/reference-semantics"
  boundary_status=1
else
  printf 'OK: %s is absent\n' "$reference_root/reference-semantics"
  boundary_status=0
fi

printf '\nTrusted/candidate prompt comparison\n'
cmp "$reference_root/prompt.py" "$candidate_root/prompt.py"
printf 'prompt_cmp_status=%d\n' "$?"

printf '\nTrusted/candidate translator comparison\n'
cmp "$reference_root/py2mpy.py" "$candidate_root/py2mpy.py"
printf 'translator_cmp_status=%d\n' "$?"

printf '\nRequired source artifact types\n'
required=(
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
  prove.sh
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
)
artifact_status=0
for rel in "${required[@]}"; do
  path="$candidate_root/$rel"
  if [[ -L "$path" ]]; then
    printf 'FAIL symlink %s -> %s\n' "$path" "$(readlink "$path")"
    artifact_status=1
  elif [[ ! -f "$path" ]]; then
    printf 'FAIL missing-or-mistyped %s\n' "$path"
    artifact_status=1
  else
    printf 'OK regular-file %s size=%s sha256=%s\n' \
      "$path" "$(stat -c %s "$path")" "$(sha256sum "$path" | cut -d' ' -f1)"
  fi
done

printf '\nCandidate symlinks (all depths)\n'
find "$candidate_root" -type l -printf '%p -> %l\n'

printf '\nStructured generation traces\n'
trace_count=0
while IFS= read -r -d '' trace; do
  trace_count=$((trace_count + 1))
  printf 'TRACE regular-file=%s size=%s sha256=%s lines=%s\n' \
    "$trace" "$(stat -c %s "$trace")" "$(sha256sum "$trace" | cut -d' ' -f1)" \
    "$(wc -l < "$trace")"
done < <(find "$candidate_root/codex-trace" -type f -name '*.jsonl' -print0 2>/dev/null)
printf 'trace_count=%d\n' "$trace_count"

if [[ "$trace_count" -eq 0 ]]; then
  artifact_status=1
fi

if [[ "$boundary_status" -ne 0 || "$artifact_status" -ne 0 ]]; then
  exit 1
fi
