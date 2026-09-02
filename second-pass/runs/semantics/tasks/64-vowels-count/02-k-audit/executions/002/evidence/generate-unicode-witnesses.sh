#!/usr/bin/env bash
set -u

cd /tmp/audit-work/proof || exit 1
python3 ./trusted/py2mpy.py ./k-unicode-claims-zero.py \
  > ./k-unicode-claims-zero.mpy
zero_status=$?
python3 ./trusted/py2mpy.py ./k-unicode-claims-one.py \
  > ./k-unicode-claims-one.mpy
one_status=$?
printf 'zero_translation_exit=%d\n' "$zero_status"
printf 'one_translation_exit=%d\n' "$one_status"
sha256sum ./k-unicode-claims-zero.mpy ./k-unicode-claims-one.mpy
if (( zero_status != 0 )); then
  exit "$zero_status"
fi
exit "$one_status"
