#!/usr/bin/env bash
set -u

required_candidate_files=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification-core.k
  verification.k
  loop-lemma-spec.k
  spec.k
  prove.sh
)

printf 'GENERATED_SEMANTICS boundary\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'BREACH: /reference/reference-semantics exists\n'
  boundary_status=1
else
  printf 'OK: /reference/reference-semantics is absent\n'
  boundary_status=0
fi

printf '\nTrusted mount entries\n'
find /reference -maxdepth 1 -printf '%y %f -> %l\n' | sort

printf '\nCandidate required artifacts\n'
artifact_status=0
for artifact in "${required_candidate_files[@]}"; do
  path="/candidate/$artifact"
  if [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$artifact" "$(readlink "$path")"
    artifact_status=1
  elif [[ -f "$path" ]]; then
    printf 'REGULAR %s\n' "$artifact"
  elif [[ -e "$path" ]]; then
    printf 'MISTYPED %s\n' "$artifact"
    artifact_status=1
  else
    printf 'MISSING %s\n' "$artifact"
    artifact_status=1
  fi
done

printf '\nAll symlinks below candidate\n'
candidate_links=$(find /candidate -type l -print)
if [[ -n "$candidate_links" ]]; then
  printf '%s\n' "$candidate_links"
  artifact_status=1
else
  printf 'NONE\n'
fi

printf '\nCandidate top-level entries (extras included)\n'
find /candidate -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort

printf '\nTrusted/candidate identity checks\n'
cmp -s /reference/prompt.py /candidate/prompt.py
prompt_status=$?
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
printf 'prompt.py cmp status: %d\n' "$prompt_status"
printf 'py2mpy.py cmp status: %d\n' "$translator_status"
sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py

printf '\nStructured metadata syntax\n'
python3 -m json.tool /candidate/run-input.json >/dev/null
run_input_status=$?
python3 -m json.tool /candidate/metrics.json >/dev/null
metrics_status=$?
printf 'run-input.json parse status: %d\n' "$run_input_status"
printf 'metrics.json parse status: %d\n' "$metrics_status"

if (( boundary_status || artifact_status || prompt_status || translator_status ||
      run_input_status || metrics_status )); then
  exit 1
fi
