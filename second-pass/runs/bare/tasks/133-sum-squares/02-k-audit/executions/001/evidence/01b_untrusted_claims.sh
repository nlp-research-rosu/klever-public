#!/usr/bin/env bash
set -u

log=/audit-output/evidence/01b_untrusted_claims.log
exec > >(tee "$log") 2>&1

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

run sed -n '1,200p' /candidate/run-input.json
run sed -n '1,200p' /candidate/metrics.json
run sed -n '1,200p' /candidate/codex-last.txt
run rg -n -m 160 \
  'RESULT:|#Top|WarnStuckClaimState|\\[Error\\]|timed_out|exit_code|kprove|kompile|krun' \
  /candidate/codex-output.log
run wc -lc /candidate/codex-output.log
