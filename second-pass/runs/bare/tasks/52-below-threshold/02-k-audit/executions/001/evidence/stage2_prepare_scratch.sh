#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/reconstruction
if [[ -e "$scratch" || -L "$scratch" ]]; then
  echo "Refusing to overwrite existing scratch target: $scratch" >&2
  exit 73
fi
mkdir -p "$scratch"

for name in solution.py solution.mpy semantic.k verification.k spec.k prove.sh; do
  cp --no-preserve=mode,ownership,timestamps "/candidate/$name" "$scratch/$name"
done
cp --no-preserve=mode,ownership,timestamps /reference/canonical.py "$scratch/trusted-canonical.py"
cp --no-preserve=mode,ownership,timestamps /reference/prompt.py "$scratch/trusted-prompt.py"
cp --no-preserve=mode,ownership,timestamps /reference/py2mpy.py "$scratch/trusted-py2mpy.py"

find -P "$scratch" -maxdepth 1 -type f -printf '%f | %s bytes\n' | sort
sha256sum "$scratch"/*

cd "$scratch"
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
cmp_status=$?
echo "trusted translator regenerated/submitted solution.mpy cmp status: $cmp_status"
sha256sum regenerated-solution.mpy solution.mpy
exit "$cmp_status"
