#!/usr/bin/env bash
set +e
set -x

test ! -e /reference/reference-semantics
mode_boundary_status=$?
printf 'GENERATED_SEMANTICS boundary exit: %s\n' "$mode_boundary_status"

find /candidate -maxdepth 5 -printf '%y %m %s %p -> %l\n' | sort
find /reference -maxdepth 2 -printf '%y %m %s %p -> %l\n' | sort

sha256sum \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k

cmp /candidate/prompt.py /reference/prompt.py
printf 'prompt byte comparison exit: %s\n' "$?"
cmp /candidate/py2mpy.py /reference/py2mpy.py
printf 'translator byte comparison exit: %s\n' "$?"

for artifact in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-30-04-019f8997-0a34-7ee0-9e2f-79a643c89e58.jsonl
do
  test -f "$artifact" -a ! -L "$artifact"
  printf 'regular non-symlink check %s exit: %s\n' "$artifact" "$?"
  sha256sum "$artifact"
done

jq . /candidate/run-input.json
printf 'run-input parse exit: %s\n' "$?"
jq . /candidate/metrics.json
printf 'metrics parse exit: %s\n' "$?"
sed -n '1,240p' /candidate/codex-last.txt
printf 'codex-last read exit: %s\n' "$?"

# Read the complete large, untrusted logs while emitting only bounded summaries.
wc -lc /candidate/codex-output.log
sed -n '1,80p' /candidate/codex-output.log
tail -n 120 /candidate/codex-output.log
grep -nE '(^|[^[:alpha:]])(kompile|kprove|krun)([^[:alpha:]]|$)|#Top|WarnStuckClaimState|VERDICT|LEGIT' \
  /candidate/codex-output.log | tail -n 240
printf 'codex-output bounded review exit: %s\n' "$?"

trace=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-30-04-019f8997-0a34-7ee0-9e2f-79a643c89e58.jsonl
jq -s '{
  line_count: length,
  top_level_types: (group_by(.type) | map({type: .[0].type, count: length})),
  first_timestamp: (.[0].timestamp // null),
  last_timestamp: (.[-1].timestamp // null)
}' "$trace"
printf 'structured trace complete parse exit: %s\n' "$?"
sed -n '1,3p' "$trace"
tail -n 8 "$trace"

exit "$mode_boundary_status"
