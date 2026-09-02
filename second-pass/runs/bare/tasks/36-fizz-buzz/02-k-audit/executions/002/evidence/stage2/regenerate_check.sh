#!/usr/bin/env bash
set -u
set -o pipefail

scratch_root="/tmp/audit-work/36-fizz-buzz-audit-002"
generated_path="$scratch_root/candidate/solution.trusted-regenerated.mpy"

python3 "$scratch_root/trusted/py2mpy.py" \
  "$scratch_root/candidate/solution.py" > "$generated_path"
translator_status="$?"
printf 'translator_exit=%s\n' "$translator_status"
if [[ "$translator_status" -ne 0 ]]; then
  exit "$translator_status"
fi

cmp "$generated_path" "$scratch_root/candidate/solution.mpy"
compare_status="$?"
printf 'byte_identity_exit=%s\n' "$compare_status"
sha256sum "$generated_path" "$scratch_root/candidate/solution.mpy"
exit "$compare_status"
