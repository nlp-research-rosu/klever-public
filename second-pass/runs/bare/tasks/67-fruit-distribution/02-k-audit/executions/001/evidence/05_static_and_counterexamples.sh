#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'REVIEWED SOURCE WITH LINE NUMBERS:\n'
run nl -ba /tmp/audit-work/fresh/semantic.k
run nl -ba /tmp/audit-work/fresh/verification.k
run nl -ba /tmp/audit-work/fresh/spec.k

printf 'LOCAL DECLARATION/RULE COUNTS:\n'
run grep -E -n '^[[:space:]]*(syntax|configuration|rule|claim)' \
  /tmp/audit-work/fresh/semantic.k \
  /tmp/audit-work/fresh/verification.k \
  /tmp/audit-work/fresh/spec.k
run grep -E -n '\[(function|total|functional|simplification|concrete|priority|owise|macro|strict|seqstrict)' \
  /tmp/audit-work/fresh/semantic.k \
  /tmp/audit-work/fresh/verification.k \
  /tmp/audit-work/fresh/spec.k

printf 'INSTALLED K STRING HOOK CONTRACT:\n'
run sed -n 1746,1771p /usr/include/kframework/builtin/domains.md
printf 'INSTALLED K RULES THAT CONSUME findString AS AN ABSOLUTE INDEX:\n'
run sed -n 1895,1905p /usr/include/kframework/builtin/domains.md

printf 'CONCRETE INTENDED-DOMAIN WHITESPACE WITNESSES:\n'
run python3 -c \
  'from importlib.util import module_from_spec,spec_from_file_location; tests=[("5   apples and   6 oranges",19),("   5 apples and 6 oranges   ",19)]; p="/tmp/audit-work/fresh/solution.py"; s=spec_from_file_location("candidate_ws",p); m=module_from_spec(s); s.loader.exec_module(m); print([m.fruit_distribution(*x) for x in tests]); p="/reference/canonical.py"; s=spec_from_file_location("canonical_ws",p); m=module_from_spec(s); s.loader.exec_module(m); print([m.fruit_distribution(*x) for x in tests])'
run krun audit-verification-whitespace.mpy \
  --definition audit-verification-kompiled \
  --output pretty
run krun audit-verification-leading-space.mpy \
  --definition audit-verification-kompiled \
  --output pretty
