#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: $0 LOG COMMAND [ARG ...]" >&2
  exit 2
fi

log_path=$1
shift

exec script -q -e -c "$(printf '%q ' "$@")" "$log_path"
