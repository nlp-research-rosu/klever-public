#!/usr/bin/env bash
set -euo pipefail
set -x

definition_path=/tmp/audit-work/concrete-kompiled
program_path=/tmp/audit-work/source/solution.mpy

python3 /audit-output/evidence/concrete_oracle.py /reference/canonical.py

krun "$program_path" --definition "$definition_path" \
  -cARGS='pyList(.List)' \
  --pattern '<result> result(pyList(.List)) </result>'

krun "$program_path" --definition "$definition_path" \
  -cARGS='pyList(ListItem(pyInt(0)))' \
  --pattern '<result> result(pyList(ListItem(pyInt(1)))) </result>'

krun "$program_path" --definition "$definition_path" \
  -cARGS='pyList(ListItem(pyInt(-2)) ListItem(pyInt(0)) ListItem(pyInt(5)))' \
  --pattern '<result> result(pyList(ListItem(pyInt(-1)) ListItem(pyInt(1)) ListItem(pyInt(6)))) </result>'

krun "$program_path" --definition "$definition_path" \
  -cARGS='pyList(ListItem(pyInt(1)) ListItem(pyInt(2)) ListItem(pyInt(3)))' \
  --pattern '<result> result(pyList(ListItem(pyInt(2)) ListItem(pyInt(3)) ListItem(pyInt(4)))) </result>'

krun "$program_path" --definition "$definition_path" \
  -cARGS='pyList(ListItem(pyInt(100000000000000000000000000000000000000000000000000)) ListItem(pyInt(-100000000000000000000000000000000000000000000000000)))' \
  --pattern '<result> result(pyList(ListItem(pyInt(100000000000000000000000000000000000000000000000001)) ListItem(pyInt(-99999999999999999999999999999999999999999999999999)))) </result>'
