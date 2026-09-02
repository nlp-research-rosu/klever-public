#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'AUDIT STAGE 1: INPUT AND PROVENANCE INTEGRITY\n'
run date --iso-8601=seconds
run find /reference -maxdepth 3 -printf '%y %p -> %l\n'
run test ! -e /reference/reference-semantics
run test ! -L /reference/reference-semantics

required=(
  /candidate/run-input.json
  /candidate/metrics.json
  /candidate/codex-last.txt
  /candidate/codex-output.log
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/semantic.k
  /candidate/spec.k
  /candidate/verification.k
  /candidate/prove.sh
)

printf '\nRequired artifact types:\n'
missing=0
for path in "${required[@]}"; do
  if [[ -e "$path" || -L "$path" ]]; then
    run stat --printf='%F %a %s %n\n' "$path"
  else
    printf 'MISSING %s\n' "$path"
    missing=1
  fi
done
printf 'required_missing=%d\n' "$missing"

trace_count=$(find /candidate/codex-trace -type f -name '*.jsonl' 2>/dev/null | wc -l)
printf 'structured_trace_jsonl_count=%d\n' "$trace_count"
run find /candidate/codex-trace -type f -printf '%y %p -> %l\n'

printf '\nSymlinks anywhere in candidate:\n'
run find /candidate -type l -printf '%p -> %l\n'

run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/spec.k /candidate/verification.k
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py

printf '\nUntrusted run-input.json:\n'
run sed -n 1,240p /candidate/run-input.json
printf '\nUntrusted metrics.json:\n'
run sed -n 1,240p /candidate/metrics.json
printf '\nUntrusted codex-last.txt:\n'
run sed -n 1,240p /candidate/codex-last.txt
printf '\nUntrusted codex-output.log boundary:\n'
run wc -l -c /candidate/codex-output.log
run sed -n 1,80p /candidate/codex-output.log
run tail -80 /candidate/codex-output.log

trace=$(find /candidate/codex-trace -type f -name '*.jsonl' | sort | head -1)
printf '\nUntrusted structured trace boundary: %s\n' "$trace"
run wc -l -c "$trace"
run sed -n 1,5p "$trace"
run tail -5 "$trace"
