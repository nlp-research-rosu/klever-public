#!/usr/bin/env bash
set -euo pipefail
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/35-max-element

echo "LOCAL_SYNTAX_DECLARATION_LINES"
rg -n '^[[:space:]]*syntax ' semantic.k verification.k
echo "LOCAL_RULE_LINES"
rg -n '^[[:space:]]*rule ' semantic.k verification.k
echo "LOCAL_CLAIM_LINES"
rg -n '^[[:space:]]*claim([[:space:]]|$)' spec.k
echo "SPECIAL_ATTRIBUTE_LINES"
rg -n 'function|functional|total|opaque|priority|simplification|concrete|macro|anywhere' \
  semantic.k verification.k spec.k

krun shadow-max.mpy \
  --definition audit-semantic-kompiled \
  --color off \
  -cARGS='[1, 2]'
python3 - <<'PY'
def max_element(max):
    return max(max)

try:
    max_element([1, 2])
except Exception as err:
    print(f"SHADOW_PYTHON_EXCEPTION={type(err).__name__}: {err}")
else:
    raise AssertionError("shadow witness unexpectedly returned")
PY

krun trailing-return.mpy \
  --definition audit-semantic-kompiled \
  --color off \
  -cARGS='[1, 2]'
python3 - <<'PY'
def max_element(l):
    return max(l)
    return max(l)

print(f"TRAILING_RETURN_PYTHON_RESULT={max_element([1, 2])}")
PY
