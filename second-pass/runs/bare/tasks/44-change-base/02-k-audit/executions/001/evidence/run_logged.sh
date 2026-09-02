#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
log_path="/audit-output/evidence/${log_name}"

{
  printf 'CWD: %q\n' "$PWD"
  printf 'PATH_SETUP: export PATH=%q\n' "${HOME}/.nix-profile/bin:\$PATH"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_path"

export PATH="${HOME}/.nix-profile/bin:${PATH}"
set +e
"$@" 2>&1 | tee -a "$log_path"
command_status=${PIPESTATUS[0]}
set -e
printf 'EXIT_STATUS: %d\n' "$command_status" | tee -a "$log_path"
exit "$command_status"
