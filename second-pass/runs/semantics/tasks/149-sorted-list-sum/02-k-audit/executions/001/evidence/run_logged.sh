#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
evidence_dir=/audit-output/evidence
scratch_log=/tmp/audit-work/"${label}.full.log"
command_file="${evidence_dir}/${label}.cmd"
bounded_log="${evidence_dir}/${label}.log"
status_file="${evidence_dir}/${label}.status"

{
  printf 'cwd=%q\n' "$PWD"
  printf 'command='
  printf '%q ' "$@"
  printf '\n'
} > "$command_file"

"$@" > "$scratch_log" 2>&1
status=$?

line_count=$(wc -l < "$scratch_log")
{
  printf 'captured_lines=%s\n' "$line_count"
  if (( line_count <= 320 )); then
    sed -n '1,320p' "$scratch_log"
  else
    sed -n '1,220p' "$scratch_log"
    printf '\n[... %s lines omitted from bounded audit log ...]\n\n' "$((line_count - 320))"
    tail -n 100 "$scratch_log"
  fi
} > "$bounded_log"
printf '%s\n' "$status" > "$status_file"

cat "$bounded_log"
printf 'exit_status=%s\n' "$status"
exit "$status"
