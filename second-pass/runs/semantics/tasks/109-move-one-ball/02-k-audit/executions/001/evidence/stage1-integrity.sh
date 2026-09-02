#!/usr/bin/env bash
set +e

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n\n' "$status"
}

run test -d /reference/reference-semantics
run find /candidate -type l -printf '%p -> %l\n'
run find /candidate -maxdepth 1 -printf '%y %f\n'
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
run bash -lc "cd /candidate/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum"
run bash -lc "cd /reference/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum"
run bash -lc "for f in run-input.json metrics.json codex-last.txt codex-output.log; do if test -e /candidate/\$f; then printf 'present %s\\n' \"\$f\"; else printf 'missing %s\\n' \"\$f\"; fi; done"
run bash -lc "find /candidate -maxdepth 1 -type f \\( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*events*' \\) -printf '%f\\n'"
