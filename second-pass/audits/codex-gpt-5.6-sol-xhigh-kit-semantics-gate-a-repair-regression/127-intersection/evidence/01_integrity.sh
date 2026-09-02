#!/usr/bin/env bash
set -u

status=0

run_check() {
  printf '\n$ %s\n' "$*"
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
}

printf 'Semantics mode: SUPPLIED_SEMANTICS\n'
run_check test -d /reference/reference-semantics
run_check test ! -L /reference/reference-semantics
run_check test -d /candidate/reference-semantics
run_check test ! -L /candidate/reference-semantics
run_check test -f /reference/prompt.py
run_check test -f /reference/canonical.py
run_check test -f /reference/py2mpy.py
run_check test -f /candidate/prompt.py
run_check test -f /candidate/py2mpy.py
run_check cmp -s /candidate/prompt.py /reference/prompt.py
run_check cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run_check diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics

printf '\n$ find -P /candidate -type l -print\n'
candidate_links=$(find -P /candidate -type l -print)
rc=$?
printf '%s' "$candidate_links"
if [[ -n "$candidate_links" ]]; then
  printf '\n'
  status=1
fi
printf '[exit %d; symlinks=%s]\n' "$rc" "$([[ -n "$candidate_links" ]] && printf present || printf none)"

printf '\nRequired candidate source artifact types:\n'
for path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k
do
  printf '$ stat -c "%%F %%n" %s\n' "$path"
  if [[ -f "$path" && ! -L "$path" ]]; then
    stat -c '%F %n' "$path"
    printf '[exit 0]\n'
  else
    stat -c '%F %n' "$path" 2>&1 || true
    printf '[integrity failure]\n'
    status=1
  fi
done

printf '\nTrusted/candidate hashes:\n'
sha256sum \
  /reference/prompt.py \
  /candidate/prompt.py \
  /reference/py2mpy.py \
  /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k

printf '\nReference semantics regular-file manifest:\n'
find -P /reference/reference-semantics -type f -print0 |
  sort -z |
  xargs -0 sha256sum

printf '\nCandidate semantics regular-file manifest:\n'
find -P /candidate/reference-semantics -type f -print0 |
  sort -z |
  xargs -0 sha256sum

printf '\nOVERALL_INTEGRITY_STATUS=%d\n' "$status"
exit "$status"
