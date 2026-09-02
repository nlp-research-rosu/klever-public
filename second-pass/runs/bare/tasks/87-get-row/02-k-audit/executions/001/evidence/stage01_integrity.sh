#!/usr/bin/env bash
set -u

status=0

printf '%s\n' '$ test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics'
test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
rc=$?
printf 'exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ stat required trusted and candidate artifacts'
for path in \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
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
  stat -c '%F|mode=%a|size=%s|%n|target=%N' "$path"
  rc=$?
  printf 'exit=%d path=%s\n' "$rc" "$path"
  if (( rc != 0 )); then status=1; fi
done

printf '%s\n' '$ find candidate source/provenance scope for symlinks'
find /candidate -maxdepth 1 -type l -printf '%p -> %l\n'
rc=$?
printf 'exit=%d\n' "$rc"
(( rc == 0 )) || status=1
find /candidate/codex-trace -type l -printf '%p -> %l\n'
rc=$?
printf 'trace_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ cmp trusted prompt and translator with candidate copies'
cmp -s /reference/prompt.py /candidate/prompt.py
rc=$?
printf 'prompt_cmp_exit=%d\n' "$rc"
(( rc == 0 )) || status=1
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
rc=$?
printf 'translator_cmp_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ sha256sum trusted and candidate identity inputs'
sha256sum \
  /reference/canonical.py \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
rc=$?
printf 'exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ cmp every scratch execution source with its read-only origin'
for name in solution.py solution.mpy semantic.k verification.k spec.k prove.sh
do
  cmp -s "/candidate/$name" "/tmp/audit-work/87-get-row/source/$name"
  rc=$?
  printf 'candidate_scratch_cmp_exit=%d file=%s\n' "$rc" "$name"
  (( rc == 0 )) || status=1
done
for name in canonical.py prompt.py py2mpy.py
do
  cmp -s "/reference/$name" "/tmp/audit-work/87-get-row/source/$name"
  rc=$?
  printf 'trusted_scratch_cmp_exit=%d file=%s\n' "$rc" "$name"
  (( rc == 0 )) || status=1
done

printf 'overall_exit=%d\n' "$status"
exit "$status"
