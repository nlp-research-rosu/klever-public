#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  set +e
  "$@"
  status=$?
  set -e
  printf '[exit %d]\n' "$status"
}

set -e

run pwd
run find /reference -xdev -maxdepth 3 -printf '%y %m %s %p -> %l\n'
run find /candidate -xdev -maxdepth 4 -printf '%y %m %s %p -> %l\n'
run find /candidate -xdev -type l -printf '%p -> %l\n'
run test ! -e /reference/reference-semantics
run test -f /reference/prompt.py
run test -f /reference/canonical.py
run test -f /reference/py2mpy.py

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k spec.k prove.sh
do
  run test -f "/candidate/$artifact"
  run test ! -L "/candidate/$artifact"
done

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k \
  /candidate/run-input.json /candidate/metrics.json /candidate/codex-last.txt \
  /candidate/codex-output.log

run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json
run sed -n 1,240p /candidate/codex-last.txt
run find /candidate/codex-trace -xdev -type f -printf '%s %p\n'
run sha256sum /candidate/codex-trace/2026/07/22/rollout-2026-07-22T07-21-24-019f89c6-0973-7943-8ce6-9ee05af209a5.jsonl

run bash -lc 'export PATH="$HOME/.nix-profile/bin:$PATH"; command -v kup; command -v kompile; command -v krun; command -v kprove'
run bash -lc 'export PATH="$HOME/.nix-profile/bin:$PATH"; kompile --version; kprove --version; krun --version'
