#!/usr/bin/env bash
set -u

echo "== trusted translator AST for solution.py =="
python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py --ast
echo "== local declaration/rule index =="
rg -n '^[[:space:]]*(configuration|syntax|rule|claim)|\[(function|total|functional|simplification|concrete|owise|priority)' \
  /tmp/audit-work/reconstruction/semantic.k \
  /tmp/audit-work/reconstruction/verification.k \
  /tmp/audit-work/reconstruction/spec.k
echo "== semantic.k, complete numbered source =="
nl -ba /tmp/audit-work/reconstruction/semantic.k
echo "== verification.k, complete numbered source =="
nl -ba /tmp/audit-work/reconstruction/verification.k
echo "== spec.k, complete numbered source =="
nl -ba /tmp/audit-work/reconstruction/spec.k
