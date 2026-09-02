#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

krun /audit-output/evidence/primitive_string_witness.run \
  --definition /tmp/audit-work/audit149/semantic-kompiled
status=$?
printf 'KRUN_EXIT=%s\n' "$status"
printf 'CPYTHON_LEN_EMOJI='
python3 -c 'print(len("😀"))'
exit "$status"
