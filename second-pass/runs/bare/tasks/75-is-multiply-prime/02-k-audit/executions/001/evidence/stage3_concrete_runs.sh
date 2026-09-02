#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/rebuild
runner=/audit-output/evidence/run_logged.sh

"$runner" /audit-output/evidence/stage3-krun-a30.log \
  krun solution.mpy --definition concrete-kompiled -cARG=30
"$runner" /audit-output/evidence/stage3-krun-a10.log \
  krun solution.mpy --definition concrete-kompiled -cARG=10
"$runner" /audit-output/evidence/stage3-krun-a0.log \
  krun solution.mpy --definition concrete-kompiled -cARG=0
"$runner" /audit-output/evidence/stage3-krun-a8.log \
  krun solution.mpy --definition concrete-kompiled -cARG=8
"$runner" /audit-output/evidence/stage3-krun-a97.log \
  krun solution.mpy --definition concrete-kompiled -cARG=97
"$runner" /audit-output/evidence/stage3-krun-a98.log \
  krun solution.mpy --definition concrete-kompiled -cARG=98
"$runner" /audit-output/evidence/stage3-krun-a99.log \
  krun solution.mpy --definition concrete-kompiled -cARG=99
"$runner" /audit-output/evidence/stage3-krun-a-minus7.log \
  krun solution.mpy --definition concrete-kompiled -cARG=-7
