#!/usr/bin/env bash
set -u

status=0

echo "command: find /candidate -maxdepth 1 -type f -name *.k"
find /candidate -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

for path in /candidate/semantic.k /candidate/verification.k /candidate/spec.k /candidate/solution.mpy; do
  echo "command: nl -ba $path"
  nl -ba "$path"
  rc=$?
  echo "exit: $rc"
  if (( rc != 0 )); then status=1; fi
done

echo "command: rg -n declaration/rule/claim/attribute inventory"
rg -n \
  '(^[[:space:]]*(syntax|configuration|rule|claim)|\[(function|total|functional|simplification|priority|owise|anywhere|macro|alias|symbol))' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "command: rg -n proof-risk attributes (expected no matches; rg exit 1)"
rg -n \
  '\[(total|functional|simplification|priority|owise|anywhere|macro|alias)|\[concrete|\[symbolic|fresh|opaque' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
rc=$?
echo "exit: $rc"
if (( rc != 1 )); then status=1; fi

echo "command: constructor/operator inventory from submitted solution.mpy"
rg -o \
  'Module|FuncDef|Params|Expr|Str|If|Compare|Name|CmpOp|Int|Return|BinOp|"=="|"\*"|"\*\*"|"-"' \
  /candidate/solution.mpy | sort | uniq -c
rc=$?
echo "exit: $rc"
if (( rc != 0 )); then status=1; fi

echo "script_exit: $status"
exit "$status"
