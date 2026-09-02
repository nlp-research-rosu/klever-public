#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit_status] %d\n' "$status"
  return "$status"
}

printf 'Audit stage 1: input and provenance integrity\n'
printf 'Rendered mode: GENERATED_SEMANTICS\n'

run test ! -e /reference/reference-semantics
run find /reference -maxdepth 2 -printf '%y %p -> %l\n'
run find /candidate -maxdepth 8 -printf '%y %p -> %l\n'
run find /candidate -type l -printf '%p -> %l\n'

for required in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k \
  verification.k spec.k prove.sh
do
  run test -f "/candidate/$required"
done

run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k

printf '\nUntrusted runner claims (read only; not validation evidence)\n'
run sed -n 1,120p /candidate/run-input.json
run sed -n 1,120p /candidate/metrics.json
run sed -n 1,120p /candidate/codex-last.txt
run wc -l -c /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-34-08-019f8963-d311-7600-88de-0356008e00ef.jsonl
run sh -c 'sed -n "1,45p" /candidate/codex-output.log; tail -n 45 /candidate/codex-output.log'
run sh -c 'rg -n "(#Top|WarnStuckClaimState|\\[Error\\]|RESULT:)" /candidate/codex-output.log | tail -n 80'
run python3 /audit-output/evidence/trace_summary.py
run sh -c 'tail -n 3 /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-34-08-019f8963-d311-7600-88de-0356008e00ef.jsonl'
