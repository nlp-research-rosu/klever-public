#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: capture-command.sh LOG COMMAND [ARG ...]" >&2
  exit 64
fi

log_path=$1
shift
tmp_output=$(mktemp /tmp/audit-capture.XXXXXX)
timeout_seconds=${AUDIT_COMMAND_TIMEOUT_SECONDS:-900}

started=$(date --iso-8601=seconds)
timeout --preserve-status "$timeout_seconds" "$@" >"$tmp_output" 2>&1
status=$?
finished=$(date --iso-8601=seconds)
byte_count=$(wc -c <"$tmp_output")

{
  printf 'STARTED: %s\n' "$started"
  printf 'FINISHED: %s\n' "$finished"
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'TIMEOUT_SECONDS: %s\n' "$timeout_seconds"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\nEXIT_STATUS: %s\n' "$status"
  printf 'OUTPUT_BYTES: %s\n' "$byte_count"
  printf '%s\n' '--- OUTPUT BEGIN ---'
  if (( byte_count <= 200000 )); then
    sed -n '1,$p' "$tmp_output"
  else
    head -c 100000 "$tmp_output"
    printf '\n--- OUTPUT TRUNCATED: middle omitted; last 100000 bytes follow ---\n'
    tail -c 100000 "$tmp_output"
  fi
  printf '%s\n' '--- OUTPUT END ---'
} >"$log_path"

rm -f "$tmp_output"
exit "$status"
