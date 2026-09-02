#!/usr/bin/env bash
set +e

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n\n' "$status"
  return "$status"
}

run_shell() {
  printf '$ %s\n' "$1"
  bash -o pipefail -c "$1"
  status=$?
  printf '[exit %d]\n\n' "$status"
  return "$status"
}

cd /tmp/audit-work/109-move-one-ball/candidate || exit 90
export PATH="$HOME/.nix-profile/bin:$PATH"

run_shell "python3 /reference/py2mpy.py auditor-concrete.py > auditor-concrete.mpy"
translation_status=$?

run krun auditor-concrete.mpy \
  --definition runtime-kompiled \
  --output pretty
krun_status=$?

printf 'translation_status=%d\n' "$translation_status"
printf 'krun_status=%d\n' "$krun_status"
if (( translation_status != 0 || krun_status != 0 )); then
  exit 1
fi
