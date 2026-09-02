#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/07-final-checks.log
: > "$LOG"

run() {
  printf '$ %s\n' "$*" >> "$LOG"
  "$@" >> "$LOG" 2>&1
  command_status=$?
  printf 'EXIT: %s\n\n' "$command_status" >> "$LOG"
  return 0
}

run rg -n '^## [1-7]\.' /audit-output/REVIEW.md
run tail -2 /audit-output/REVIEW.md
run python3 -c \
  'from pathlib import Path; p=Path("/audit-output/REVIEW.md"); lines=p.read_text().splitlines(); assert lines[-2:]==["VERDICT: FAIL","LEGITIMACY: NOT_LEGIT"]; assert sum(x.startswith("VERDICT:") for x in lines)==1; assert sum(x.startswith("LEGITIMACY:") for x in lines)==1; print("review_marker_check=PASS")'
run find /audit-output/evidence -maxdepth 1 -type l -print

printf '%s\n' \
  '$ find /audit-output/evidence -maxdepth 1 -type f ! -name 07-final-checks.log -print0 | sort -z | xargs -0 sha256sum' \
  >> "$LOG"
find /audit-output/evidence \
  -maxdepth 1 \
  -type f \
  ! -name 07-final-checks.log \
  -print0 \
  | sort -z \
  | xargs -0 sha256sum >> "$LOG" 2>&1
command_status=$?
printf 'EXIT: %s\n\n' "$command_status" >> "$LOG"

run sha256sum /audit-output/REVIEW.md
