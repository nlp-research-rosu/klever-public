#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/stage3_prepare_variants.log
exec > >(tee "$log") 2>&1

translate() {
  source_path=$1
  output_path=$2
  printf '$ python3 /tmp/audit-work/source/py2mpy.py %q > %q\n' \
    "$source_path" "$output_path"
  python3 /tmp/audit-work/source/py2mpy.py "$source_path" > "$output_path"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

translate \
  /audit-output/evidence/observe_continuation.py \
  /tmp/audit-work/source/observe_continuation.mpy || exit $?
translate \
  /audit-output/evidence/body_mutation.py \
  /tmp/audit-work/source/body_mutation.mpy || exit $?

sha256sum \
  /candidate/semantic.k \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/semantic-generic.k \
  /tmp/audit-work/source/observe_continuation.mpy \
  /tmp/audit-work/source/body_mutation.mpy

