#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 OUTPUT_PREFIX COMMAND [ARG ...]" >&2
  exit 2
fi

output_prefix=$1
shift

printf '%q ' "$@" > "${output_prefix}.cmd"
printf '\n' >> "${output_prefix}.cmd"

started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf 'started_utc=%s\n' "$started" > "${output_prefix}.meta"

set +e
"$@" > "${output_prefix}.log" 2>&1
status=$?
set -e

finished=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf '%s\n' "$status" > "${output_prefix}.status"
printf 'finished_utc=%s\n' "$finished" >> "${output_prefix}.meta"

sed -n '1,240p' "${output_prefix}.log"
exit "$status"
