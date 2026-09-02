#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/source
definition=/tmp/audit-work/build/concrete-kompiled

# These configurations violate the target claim's validPositive precondition.
# They show why the representation invariant is an explicit trust/scope boundary.
krun solution.mpy --definition "$definition" -cIPART=0 -cFRAC=2 -cSCALE=1
krun solution.mpy --definition "$definition" -cIPART=-1 -cFRAC=5 -cSCALE=10

python3 -c 'from solution import truncate_number; print("python_2.0", truncate_number(2.0)); print("python_negative_0.5", truncate_number(-0.5))'
