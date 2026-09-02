#!/usr/bin/env bash
set -euo pipefail
set -x

python3 concrete_cases.py
python3 py2mpy.py concrete_cases.py > concrete_cases.mpy
krun concrete_cases.mpy --definition runtime-kompiled-fresh
