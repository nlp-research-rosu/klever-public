#!/usr/bin/env bash
set -u

for tool in kompile krun kprove python3; do
  printf 'TOOL\t%s\t%s\n' "$tool" "$(command -v "$tool")"
done
kompile --version
printf 'KOMPILE_VERSION_STATUS\t%s\n' "$?"
kprove --version
printf 'KPROVE_VERSION_STATUS\t%s\n' "$?"
python3 --version
printf 'PYTHON_VERSION_STATUS\t%s\n' "$?"

printf 'FRESH_DEFINITIONS\n'
find /tmp/audit-work/50-decode-shift/candidate-src \
  -maxdepth 1 -type d -name 'semantic-*-kompiled' \
  -printf '%f\t%TY-%Tm-%TdT%TH:%TM:%TS\n' | sort
