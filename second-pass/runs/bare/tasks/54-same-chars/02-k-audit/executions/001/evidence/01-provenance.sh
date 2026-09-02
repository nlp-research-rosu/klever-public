#!/usr/bin/env bash
set -u

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS=%d\n' "$status"
  return 0
}

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
  /candidate/solution-program.k
  /candidate/verification.k
  /candidate/spec.k
)

run test ! -e /reference/reference-semantics
run find /reference -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n'
run find /candidate -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n'
run find /candidate /reference -xdev -type l -print

for path in "${required_candidate[@]}"; do
  run test -f "$path"
  run test ! -L "$path"
  run stat -c '%F %s bytes %n' "$path"
done

run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json
run cmp /reference/prompt.py /candidate/prompt.py
run cmp /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/solution-program.k \
  /candidate/verification.k /candidate/spec.k

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-10-25-019f894e-1b9d-7780-9186-96bff14ad993.jsonl
run test -f "$trace"
run test ! -L "$trace"
run wc -lc "$trace"
run rg -n '"type":"(session_meta|task_started|task_complete)"|RESULT: KPROVE_PASSED|#Top|EXIT:0' "$trace"
run rg -n 'RESULT: KPROVE_PASSED|#Top|WarnStuck|\\[Error\\]' /candidate/codex-output.log
