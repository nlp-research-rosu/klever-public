#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/55-fib-independent-audit
cd "$scratch"

python3 py2mpy.py solution.py > regenerated-solution.mpy
sha256sum submitted-solution.mpy regenerated-solution.mpy
cmp submitted-solution.mpy regenerated-solution.mpy
printf 'BYTE_IDENTICAL submitted-solution.mpy regenerated-solution.mpy\n'
