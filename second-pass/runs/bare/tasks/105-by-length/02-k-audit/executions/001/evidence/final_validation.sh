#!/usr/bin/env bash
set +e
set -x

kompile --version
kompile_version_exit=$?
kprove --version
kprove_version_exit=$?
krun --version
krun_version_exit=$?

for script in /audit-output/evidence/*.sh
do
  bash -n "$script"
  printf 'bash syntax %s exit: %s\n' "$script" "$?"
done

export PYTHONPYCACHEPREFIX=/tmp/audit-work/reviewer-pycache
python3 -m py_compile /audit-output/evidence/*.py
python_syntax_exit=$?
printf 'reviewer Python syntax exit: %s\n' "$python_syntax_exit"

find /audit-output/evidence -maxdepth 1 -printf '%y %m %s %f -> %l\n' | sort
find /audit-output/evidence -maxdepth 1 -type l -print
symlink_count=$(find /audit-output/evidence -maxdepth 1 -type l -print | wc -l)
printf 'evidence symlink count: %s\n' "$symlink_count"

grep -n '^## [1-7]\.' /audit-output/REVIEW.md
stage_heading_count=$(grep -c '^## [1-7]\.' /audit-output/REVIEW.md)
printf 'review stage heading count: %s\n' "$stage_heading_count"
grep -nE '^VERDICT:|^LEGITIMACY:' /audit-output/REVIEW.md
tail -n 2 /audit-output/REVIEW.md

if [ "$kompile_version_exit" -ne 0 ] \
  || [ "$kprove_version_exit" -ne 0 ] \
  || [ "$krun_version_exit" -ne 0 ] \
  || [ "$python_syntax_exit" -ne 0 ] \
  || [ "$symlink_count" -ne 0 ] \
  || [ "$stage_heading_count" -ne 7 ] \
  || [ "$(grep -c '^VERDICT:' /audit-output/REVIEW.md)" -ne 1 ] \
  || [ "$(grep -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -ne 1 ] \
  || [ "$(tail -n 2 /audit-output/REVIEW.md | sed -n '1p')" != 'VERDICT: CONCERNS' ] \
  || [ "$(tail -n 2 /audit-output/REVIEW.md | sed -n '2p')" != 'LEGITIMACY: LEGIT' ]
then
  exit 1
fi
exit 0
