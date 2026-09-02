#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

printf 'Semantics mode: GENERATED_SEMANTICS\n'
run test ! -e /reference/reference-semantics
run test -f /reference/prompt.py
run test -f /reference/canonical.py
run test -f /reference/py2mpy.py

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k \
  verification.k spec.k prove.sh
do
  run test -f "/candidate/$artifact"
done

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py
run find /candidate -type l -printf 'SYMLINK %p -> %l\n'
run find /candidate -maxdepth 2 -mindepth 1 -printf '%y %p\n'
run find /candidate/codex-trace -type f -printf '%y %s %p\n'
run wc -lc \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T07-52-05-019f89e2-1d58-7402-a397-37019fa95ca8.jsonl

run bash -c \
  'python3 /reference/py2mpy.py /tmp/audit-work/rebuild/candidate-src/solution.py > /tmp/audit-work/rebuild/candidate-src/trusted-regenerated.mpy'
run cmp -s \
  /tmp/audit-work/rebuild/candidate-src/trusted-regenerated.mpy \
  /candidate/solution.mpy
run sha256sum \
  /tmp/audit-work/rebuild/candidate-src/trusted-regenerated.mpy \
  /candidate/solution.mpy
