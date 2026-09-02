#!/usr/bin/env bash
set -u

run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "[exit $status]"
  return "$status"
}

run nl -ba /tmp/audit-work/candidate/semantic.k
run nl -ba /tmp/audit-work/candidate/verification.k
run nl -ba /tmp/audit-work/candidate/spec.k

run rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim)|\[(function|total|functional|opaque|simplification|concrete|priority|owise)' \
  /tmp/audit-work/candidate/semantic.k \
  /tmp/audit-work/candidate/verification.k \
  /tmp/audit-work/candidate/spec.k

run python3 -c '
import re
from pathlib import Path

mpy = Path("/tmp/audit-work/candidate/solution.mpy").read_text()
constructors = sorted(set(re.findall(r"\b([A-Z][A-Za-z0-9]*)\s*\(", mpy)))
print("solution_constructor_symbols", constructors)
print("ordinary_rule_count", sum(
    1 for line in Path("/tmp/audit-work/candidate/semantic.k").read_text().splitlines()
    if line.lstrip().startswith("rule ")
))
print("entry_claim_count", sum(
    1 for line in Path("/tmp/audit-work/candidate/spec.k").read_text().splitlines()
    if line.lstrip().startswith("claim")
))
'
