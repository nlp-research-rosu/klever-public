#!/usr/bin/env bash
set -u

status=0

echo "command: test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics"
if test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics; then
  echo "exit: 0"
  echo "result: generated-semantics trusted boundary is intact"
else
  rc=$?
  echo "exit: $rc"
  echo "result: INFRASTRUCTURE BREACH: forbidden trusted semantics exists"
  status=1
fi

echo "command: cmp -s /candidate/prompt.py /reference/prompt.py"
cmp -s /candidate/prompt.py /reference/prompt.py
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "command: cmp -s /candidate/py2mpy.py /reference/py2mpy.py"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "command: sha256sum trusted and candidate inputs/sources"
sha256sum \
  /reference/prompt.py \
  /reference/canonical.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-55-05-019f8977-00e7-74e3-8113-548ceabd44ea.jsonl
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "command: find candidate source/provenance entries and report symlinks"
find /candidate -maxdepth 1 -printf '%y %f -> %l\n' | sort
find /candidate/codex-trace -type f -printf '%y %p -> %l\n' | sort
find /candidate -type l -printf 'SYMLINK %p -> %l\n'
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "required artifact type checks"
for path in \
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
  /candidate/prove.sh
do
  if test -f "$path" && test ! -L "$path"; then
    echo "OK regular non-symlink: $path"
  else
    echo "BAD missing, mistyped, or symlinked: $path"
    status=1
  fi
done

echo "structured trace check"
trace_count=$(find /candidate/codex-trace -type f -name '*.jsonl' | wc -l)
echo "jsonl trace files: $trace_count"
if (( trace_count < 1 )); then status=1; fi

echo "script_exit: $status"
exit "$status"
