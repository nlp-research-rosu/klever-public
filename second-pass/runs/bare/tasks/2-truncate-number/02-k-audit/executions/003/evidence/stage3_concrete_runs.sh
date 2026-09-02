#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/source
definition=/tmp/audit-work/build/concrete-kompiled

# Documented example, using the canonical exact dyadic decomposition.
krun solution.mpy --definition "$definition" -cIPART=3 -cFRAC=1 -cSCALE=2

# Positive value below one (zero integer component).
krun solution.mpy --definition "$definition" -cIPART=0 -cFRAC=1 -cSCALE=4

# Exact integer (zero fractional component).
krun solution.mpy --definition "$definition" -cIPART=1 -cFRAC=0 -cSCALE=1

# IEEE-754 values immediately below and above 1.0.
krun solution.mpy --definition "$definition" \
  -cIPART=0 -cFRAC=9007199254740991 -cSCALE=9007199254740992
krun solution.mpy --definition "$definition" \
  -cIPART=1 -cFRAC=1 -cSCALE=4503599627370496

# Integer-precision boundary.
krun solution.mpy --definition "$definition" \
  -cIPART=9007199254740992 -cFRAC=0 -cSCALE=1
