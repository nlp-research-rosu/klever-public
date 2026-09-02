#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
source_dir="$scratch/candidate-source"
trusted_dir="$scratch/trusted"

cp "$evidence/differential_test.py" "$scratch/differential_test.py"

{
  printf 'COMMAND: python3 %q %q > %q\n' \
    "$trusted_dir/py2mpy.py" "$source_dir/solution.py" \
    "$scratch/regenerated-solution.mpy"
  python3 "$trusted_dir/py2mpy.py" "$source_dir/solution.py" \
    > "$scratch/regenerated-solution.mpy"
  translate_status=$?
  printf 'EXIT_STATUS: %d\n' "$translate_status"

  printf 'COMMAND: cmp -s %q %q\n' \
    "$scratch/regenerated-solution.mpy" "$source_dir/solution.mpy"
  cmp -s "$scratch/regenerated-solution.mpy" "$source_dir/solution.mpy"
  cmp_status=$?
  printf 'EXIT_STATUS: %d\n' "$cmp_status"

  printf 'COMMAND: sha256sum %q %q\n' \
    "$scratch/regenerated-solution.mpy" "$source_dir/solution.mpy"
  sha256sum "$scratch/regenerated-solution.mpy" "$source_dir/solution.mpy"
  digest_status=$?
  printf 'EXIT_STATUS: %d\n' "$digest_status"
} > "$evidence/stage2_translation.log" 2>&1

{
  printf 'COMMAND: python3 %q %q %q\n' \
    "$scratch/differential_test.py" "$trusted_dir/canonical.py" \
    "$source_dir/solution.py"
  python3 "$scratch/differential_test.py" \
    "$trusted_dir/canonical.py" "$source_dir/solution.py"
  differential_status=$?
  printf 'EXIT_STATUS: %d\n' "$differential_status"
} > "$evidence/stage2_differential.log" 2>&1

if (( translate_status != 0 || cmp_status != 0 || digest_status != 0 ||
      differential_status != 0 )); then
  exit 1
fi
