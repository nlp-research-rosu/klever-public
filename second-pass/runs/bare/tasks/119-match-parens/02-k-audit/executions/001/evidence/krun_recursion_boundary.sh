#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/119-match-parens-audit

printf -v audit_spaces '%*s' 600 ''
audit_opens=${audit_spaces// /\(}
audit_closes=${audit_spaces// /\)}
audit_input="ListExpr(Str(\"${audit_opens}\"), Str(\"${audit_closes}\"))"

printf 'INPUT_LENGTHS: %s,%s total=%s\n' \
  "${#audit_opens}" "${#audit_closes}" \
  "$(( ${#audit_opens} + ${#audit_closes} ))"
printf '%s\n' 'PYTHON_CANDIDATE: RecursionError (see 02-differential.log)'
printf '%s\n' 'TRUSTED_CANONICAL: Yes (see 02-differential.log)'
krun solution.mpy \
  --definition semantic-kompiled-fresh \
  -cINPUT="$audit_input" |
  rg 'strVal \( (yesString|noString) \)'
