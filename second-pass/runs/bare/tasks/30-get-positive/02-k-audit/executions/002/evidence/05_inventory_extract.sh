#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive/candidate-src

printf 'SOURCE semantic.k with line numbers\n'
nl -ba "$work/semantic.k"
printf 'SOURCE verification.k with line numbers\n'
nl -ba "$work/verification.k"
printf 'SOURCE spec.k with line numbers\n'
nl -ba "$work/spec.k"

printf 'LEXICAL declaration inventory\n'
rg -n \
  '^\s*(module|imports|configuration|syntax|rule|claim|requires)|\[(function|total|functional|simplification|concrete|owise|priority|constructor|symbol)' \
  "$work/semantic.k" "$work/verification.k" "$work/spec.k"

printf 'CANONICAL verification simplification-rule inventory\n'
PYTHONPATH=/opt/humaneval python3 - <<'PY'
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification

print(json.dumps(
    inventory_verification(
        Path("/tmp/audit-work/30-get-positive/candidate-src")
    ),
    indent=2,
    sort_keys=True,
))
PY
