#!/usr/bin/env bash
set -euo pipefail

work_dir=/tmp/audit-work/reconstruction
python3 "$work_dir/py2mpy.py" "$work_dir/solution.py" \
  > "$work_dir/solution.regenerated.mpy"
cmp "$work_dir/solution.mpy" "$work_dir/solution.regenerated.mpy"
sha256sum "$work_dir/solution.mpy" "$work_dir/solution.regenerated.mpy"
echo "TRANSLATOR_BYTE_IDENTITY=PASS"
