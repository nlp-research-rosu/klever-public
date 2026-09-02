#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
scratch=/tmp/audit-work/140-fix-spaces
evidence=/audit-output/evidence
overall=0

cd "$scratch" || exit 2
cp "$evidence/independent-concrete.py" independent-concrete.py

printf '$ python3 independent-concrete.py\n'
python3 independent-concrete.py
status_python=$?
printf '[exit %d]\n' "$status_python"
if [[ "$status_python" -ne 0 ]]; then
  overall=1
fi

printf '$ python3 /reference/py2mpy.py independent-concrete.py > independent-concrete.mpy\n'
python3 /reference/py2mpy.py independent-concrete.py > independent-concrete.mpy
status_translate=$?
printf '[exit %d]\n' "$status_translate"
if [[ "$status_translate" -ne 0 ]]; then
  overall=1
fi
cp independent-concrete.mpy "$evidence/independent-concrete.mpy"

printf '$ krun independent-concrete.mpy --definition runtime-kompiled\n'
krun independent-concrete.mpy --definition runtime-kompiled
status_krun=$?
printf '[exit %d]\n' "$status_krun"
if [[ "$status_krun" -ne 0 ]]; then
  overall=1
fi

printf 'overall_exit=%d\n' "$overall"
exit "$overall"
