#!/usr/bin/env bash
set -euo pipefail
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

root=/tmp/audit-work/130-tri

python3 "$root/reference/py2mpy.py" "$root/candidate/solution.py" \
  > "$root/build/regenerated-solution.mpy"
cmp -s "$root/build/regenerated-solution.mpy" "$root/candidate/solution.mpy"
printf 'trusted_translation_byte_identity=true\n'
sha256sum "$root/build/regenerated-solution.mpy" "$root/candidate/solution.mpy"

python3 /audit-output/evidence/differential_tri.py
