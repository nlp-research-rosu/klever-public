#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/118-get-closest-vowel
trusted_generated="$scratch/trusted-regenerated.mpy"

printf 'COMMAND=python3 %q %q > %q\n' \
  "$scratch/reference/py2mpy.py" \
  "$scratch/candidate-src/solution.py" \
  "$trusted_generated"
python3 "$scratch/reference/py2mpy.py" \
  "$scratch/candidate-src/solution.py" > "$trusted_generated"
translate_status=$?
printf 'TRANSLATE_EXIT_STATUS=%s\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

printf 'COMMAND=cmp -s %q %q\n' \
  "$trusted_generated" "$scratch/candidate-src/solution.mpy"
cmp -s "$trusted_generated" "$scratch/candidate-src/solution.mpy"
cmp_status=$?
printf 'MPY_BYTE_IDENTITY_EXIT_STATUS=%s\n' "$cmp_status"
sha256sum "$trusted_generated" "$scratch/candidate-src/solution.mpy"
if (( cmp_status != 0 )); then
  exit "$cmp_status"
fi

printf 'COMMAND=python3 /audit-output/evidence/fidelity/differential.py\n'
python3 /audit-output/evidence/fidelity/differential.py
differential_status=$?
printf 'DIFFERENTIAL_EXIT_STATUS=%s\n' "$differential_status"
exit "$differential_status"
