#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'AUDIT_MODE: GENERATED_SEMANTICS\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'REFERENCE_SEMANTICS_BOUNDARY: PRESENT (infrastructure contradiction)\n'
  run stat /reference/reference-semantics
else
  printf 'REFERENCE_SEMANTICS_BOUNDARY: ABSENT (expected)\n'
fi

required_candidate=(
  /candidate/run-input.json
  /candidate/metrics.json
  /candidate/codex-last.txt
  /candidate/codex-output.log
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/semantic.k
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
)
required_reference=(
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
)

for path in "${required_candidate[@]}" "${required_reference[@]}"; do
  if [[ -L "$path" ]]; then
    printf 'ARTIFACT: %s TYPE=symlink TARGET=%s\n' "$path" "$(readlink "$path")"
  elif [[ -f "$path" ]]; then
    printf 'ARTIFACT: %s TYPE=regular SIZE=%s\n' "$path" "$(stat -c %s "$path")"
  elif [[ -e "$path" ]]; then
    printf 'ARTIFACT: %s TYPE=%s (mistyped)\n' "$path" "$(stat -c %F "$path")"
  else
    printf 'ARTIFACT: %s MISSING\n' "$path"
  fi
done

run cmp --silent /candidate/prompt.py /reference/prompt.py
run cmp --silent /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py
run find /candidate -type l -printf '%p -> %l\n'
run python3 /audit-output/evidence/01_trace_check.py

printf 'UNTRUSTED RUN METADATA:\n'
run sed -n 1,200p /candidate/run-input.json
run sed -n 1,200p /candidate/metrics.json
run sed -n 1,200p /candidate/codex-last.txt
printf 'UNTRUSTED OUTPUT SUMMARY:\n'
run wc -l /candidate/codex-output.log
run grep -E -n '(^|[^[:alpha:]])(kompile|krun|kprove)([^[:alpha:]]|$)|#Top|RESULT:' /candidate/codex-output.log
