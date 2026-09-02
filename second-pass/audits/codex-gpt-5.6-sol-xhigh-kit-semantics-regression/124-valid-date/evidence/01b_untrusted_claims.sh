#!/usr/bin/env bash
set -u

record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return "$status"
}

record wc -l -c \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/PROOF.md \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T21-40-56-019f8cd8-f2f6-7a42-bb69-3c009ceb873e.jsonl

record sha256sum \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/PROOF.md \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T21-40-56-019f8cd8-f2f6-7a42-bb69-3c009ceb873e.jsonl

record python3 - /candidate/codex-output.log <<'PY'
import collections
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
terms = (
    "#Top",
    "WarnStuckClaimState",
    "VALIDATED",
    "KPROVE_PASSED",
    "MISMATCHES=0",
    "BODY_MUTATION_PROBE_EXPECTED_FAILURE",
    "VACUITY_PROBE_EXPECTED_FAILURE",
    "ERROR",
    "timeout",
)
counts = collections.Counter()
lines = 0
for line in path.open(errors="replace"):
    lines += 1
    for term in terms:
        counts[term] += line.count(term)
print(f"fully_scanned_lines={lines}")
for term in terms:
    print(f"{term!r}={counts[term]}")
PY

record tail -n 20 /candidate/codex-output.log
