#!/usr/bin/env bash
set -u

python3 /reference/py2mpy.py /audit-output/evidence/stage4_concrete.py \
  > /audit-output/evidence/stage4_concrete.mpy
translator_status=$?
echo "translator_exit_status=$translator_status"
sha256sum /audit-output/evidence/stage4_concrete.py \
          /audit-output/evidence/stage4_concrete.mpy
exit "$translator_status"
