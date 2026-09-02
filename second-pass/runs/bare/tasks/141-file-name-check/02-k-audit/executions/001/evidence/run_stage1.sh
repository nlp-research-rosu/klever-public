#!/usr/bin/env bash
set -u

evidence=/audit-output/evidence
trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T07-26-43-019f89ca-e5fc-7482-b894-6e10d45410ce.jsonl

{
  printf '%s\n' 'COMMAND: kompile --version && kprove --version && krun --version'
  kompile --version
  kompile_version_status=$?
  kprove --version
  kprove_version_status=$?
  krun --version
  krun_version_status=$?
  printf 'EXIT_STATUS: %d\n' \
    "$(( kompile_version_status || kprove_version_status || krun_version_status ))"

  printf '%s\n' \
    'COMMAND: test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics'
  test ! -e /reference/reference-semantics &&
    test ! -L /reference/reference-semantics
  mode_status=$?
  printf 'EXIT_STATUS: %d\n' "$mode_status"

  printf '%s\n' \
    'COMMAND: cmp -s /candidate/prompt.py /reference/prompt.py'
  cmp -s /candidate/prompt.py /reference/prompt.py
  prompt_status=$?
  printf 'EXIT_STATUS: %d\n' "$prompt_status"

  printf '%s\n' \
    'COMMAND: cmp -s /candidate/py2mpy.py /reference/py2mpy.py'
  cmp -s /candidate/py2mpy.py /reference/py2mpy.py
  translator_status=$?
  printf 'EXIT_STATUS: %d\n' "$translator_status"

  printf '%s\n' \
    'COMMAND: sha256sum /candidate/prompt.py /reference/prompt.py /candidate/py2mpy.py /reference/py2mpy.py'
  sha256sum \
    /candidate/prompt.py /reference/prompt.py \
    /candidate/py2mpy.py /reference/py2mpy.py
  digest_status=$?
  printf 'EXIT_STATUS: %d\n' "$digest_status"

  printf '%s\n' \
    'COMMAND: find required artifacts for non-regular files or symlinks'
  artifact_status=0
  for path in \
    /candidate/run-input.json \
    /candidate/metrics.json \
    /candidate/codex-last.txt \
    /candidate/codex-output.log \
    "$trace" \
    /candidate/prompt.py \
    /candidate/py2mpy.py \
    /candidate/solution.py \
    /candidate/solution.mpy \
    /candidate/semantic.k \
    /candidate/verification.k \
    /candidate/spec.k \
    /reference/prompt.py \
    /reference/canonical.py \
    /reference/py2mpy.py
  do
    if [[ -f "$path" && ! -L "$path" ]]; then
      stat -c 'REGULAR mode=%a size=%s path=%n' "$path"
    else
      printf 'INTEGRITY_FAILURE path=%s\n' "$path"
      artifact_status=1
    fi
  done
  printf 'EXIT_STATUS: %d\n' "$artifact_status"

  printf '%s\n' 'COMMAND: find /candidate -maxdepth 1 -printf ... | sort'
  find /candidate -maxdepth 1 -printf '%y %f -> %l\n' | sort
  inventory_status=$?
  printf 'EXIT_STATUS: %d\n' "$inventory_status"

  printf '%s\n' \
    'COMMAND: find /candidate -type l -printf ...'
  symlink_entries=$(find /candidate -type l -printf '%p -> %l\n')
  symlink_status=$?
  if [[ -n "$symlink_entries" ]]; then
    printf '%s\n' "$symlink_entries"
    symlink_count=$(printf '%s\n' "$symlink_entries" | wc -l)
  else
    symlink_count=0
  fi
  printf 'SYMLINK_COUNT: %d\n' "$symlink_count"
  printf 'EXIT_STATUS: %d\n' "$symlink_status"

  printf '%s\n' \
    "COMMAND: wc -l -c /candidate/codex-output.log $trace"
  wc -l -c /candidate/codex-output.log "$trace"
  size_status=$?
  printf 'EXIT_STATUS: %d\n' "$size_status"

  printf '%s\n' 'UNTRUSTED run-input.json'
  sed -n '1,120p' /candidate/run-input.json
  printf '%s\n' 'UNTRUSTED metrics.json'
  sed -n '1,120p' /candidate/metrics.json
  printf '%s\n' 'UNTRUSTED codex-last.txt'
  sed -n '1,120p' /candidate/codex-last.txt
  printf '%s\n' 'UNTRUSTED codex-output.log selected terminal claims'
  rg -n \
    '(RESULT:|#Top|mutation probe|Concrete `krun`|Full `./prove.sh`)' \
    /candidate/codex-output.log | tail -n 40
  printf '%s\n' 'UNTRUSTED structured trace first/last event metadata'
  head -n 1 "$trace"
  tail -n 2 "$trace"
} > "$evidence/stage1_integrity.log" 2>&1

if (( mode_status != 0 || prompt_status != 0 || translator_status != 0 ||
      digest_status != 0 || artifact_status != 0 || inventory_status != 0 ||
      symlink_status != 0 || symlink_count != 0 || size_status != 0 ||
      kompile_version_status != 0 || kprove_version_status != 0 ||
      krun_version_status != 0 )); then
  exit 1
fi
