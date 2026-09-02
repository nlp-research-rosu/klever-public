#!/usr/bin/env bash
set -u

status=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
}

echo '== Trusted and candidate top-level inventories =='
run find -P /reference -maxdepth 3 -printf '%y %p -> %l\n'
run find -P /candidate -maxdepth 3 -printf '%y %p -> %l\n'

echo '== Required generation records =='
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "/candidate/$name" || -L "/candidate/$name" ]]; then
    run stat -c '%F %s bytes %n' "/candidate/$name"
    run sed -n '1,160p' "/candidate/$name"
  else
    printf 'MISSING /candidate/%s\n' "$name"
  fi
done
echo 'Potential structured traces:'
run find -P /candidate -maxdepth 1 -type f \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*events*' \) -printf '%f\n'

echo '== Trusted prompt and translator identity =='
run cmp -s /candidate/prompt.py /reference/prompt.py
run sha256sum /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum /candidate/py2mpy.py /reference/py2mpy.py

echo '== Supplied semantics integrity =='
if [[ ! -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  echo 'INFRASTRUCTURE BREACH: trusted supplied semantics absent or symlinked'
  exit 90
fi
if [[ ! -d /candidate/reference-semantics || -L /candidate/reference-semantics ]]; then
  echo 'CANDIDATE INTEGRITY FAILURE: candidate supplied semantics absent, mistyped, or symlinked'
  exit 1
fi
run find -P /candidate/reference-semantics -type l -printf 'SYMLINK %p -> %l\n'
run diff -r --no-dereference --brief /reference/reference-semantics /candidate/reference-semantics
run diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
run sh -c "cd /reference/reference-semantics && find -P . -printf '%y %P\\n' | LC_ALL=C sort"
run sh -c "cd /candidate/reference-semantics && find -P . -printf '%y %P\\n' | LC_ALL=C sort"

exit "$status"
