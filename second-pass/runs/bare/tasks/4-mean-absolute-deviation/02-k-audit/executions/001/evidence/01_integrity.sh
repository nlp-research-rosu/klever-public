#!/usr/bin/env bash
set -u

run() {
  local description="$1"
  shift
  printf '\nCOMMAND (%s):' "$description"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

printf 'AUDIT STAGE 1: input and provenance integrity\n'
printf 'All /candidate material is treated as untrusted evidence.\n'

run "trusted semantics-mode boundary: generated mode requires absence" \
  test ! -e /reference/reference-semantics

run "candidate prompt is byte-identical to trusted prompt" \
  cmp -s /candidate/prompt.py /reference/prompt.py

run "candidate translator is byte-identical to trusted translator" \
  cmp -s /candidate/py2mpy.py /reference/py2mpy.py

run "hash trusted and candidate provenance files" \
  sha256sum \
    /candidate/prompt.py /reference/prompt.py \
    /candidate/py2mpy.py /reference/py2mpy.py

required=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  spec.k
  verification.k
  prove.sh
)

printf '\nREQUIRED CANDIDATE ARTIFACT TYPES\n'
artifact_failure=0
for artifact in "${required[@]}"; do
  path="/candidate/$artifact"
  if [[ -L "$path" ]]; then
    printf 'SYMLINK (failure): %s -> %s\n' "$path" "$(readlink "$path")"
    artifact_failure=1
  elif [[ -f "$path" ]]; then
    stat -c 'REGULAR %a %s %n' "$path"
  elif [[ -e "$path" ]]; then
    stat -c 'MISTYPED %F %a %s %n' "$path"
    artifact_failure=1
  else
    printf 'MISSING: %s\n' "$path"
    artifact_failure=1
  fi
done
printf 'REQUIRED ARTIFACT TYPE CHECK EXIT STATUS: %d\n' "$artifact_failure"

printf '\nALL CANDIDATE SYMLINKS (must be empty)\n'
find /candidate -type l -printf '%p -> %l\n'
find_status=$?
printf 'EXIT STATUS: %d\n' "$find_status"

printf '\nSTRUCTURED TRACE INVENTORY\n'
find /candidate/codex-trace -maxdepth 8 -printf '%y %s %p\n' | sort
trace_status=$?
printf 'EXIT STATUS: %d\n' "$trace_status"

printf '\nUNTRUSTED RUN CLAIMS: run-input.json\n'
sed -n '1,200p' /candidate/run-input.json
printf '\nUNTRUSTED RUN CLAIMS: metrics.json\n'
sed -n '1,200p' /candidate/metrics.json
printf '\nUNTRUSTED FINAL CLAIM: codex-last.txt\n'
sed -n '1,200p' /candidate/codex-last.txt

printf '\nBOUNDED UNTRUSTED LOG/TRACE CLAIM EXCERPTS\n'
rg -n -m 30 '#Top|KPROVE_PASSED|kprove printed|final .*run|exit code' \
  /candidate/codex-output.log /candidate/codex-trace |
  cut -c1-1200 || true

if (( artifact_failure != 0 )); then
  exit "$artifact_failure"
fi
