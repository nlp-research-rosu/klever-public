#!/usr/bin/env bash
# kprove every VERIFICATION (proof) test under tests/verification/<case>/.
# Each <case>/ imports the shared reference semantics; the K module prefix is the
# upper-cased folder name (loop-break -> LOOP-BREAK) for the -VERIFICATION / -SPEC
# modules, while the syntax module is the shared MPY-SYNTAX (see the golden
# questions/3-below-zero). kprove is always memory-capped (kore-exec is unbounded
# — see ../../NOTES.md "Cap kprove memory").
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # reference/tests
rc=0
for d in "$HERE"/verification/*/; do
  name="$(basename "$d")"
  MOD="$(printf '%s' "$name" | tr 'a-z' 'A-Z')"        # loop-break -> LOOP-BREAK
  DEF="$d/verification-kompiled"
  if ! kompile "$d/verification.k" --backend haskell \
        --main-module "${MOD}-VERIFICATION" --syntax-module MPY-SYNTAX \
        --output-definition "$DEF" >/dev/null 2>&1; then
    printf "  %-16s KOMPILE-FAIL\n" "$name"; rc=1; continue
  fi
  out="$(systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet \
         timeout 1800 kprove "$d/spec.k" --definition "$DEF" --spec-module "${MOD}-SPEC" 2>&1)"
  if printf '%s' "$out" | grep -q '^#Top'; then printf "  %-16s #Top\n" "$name"
  else printf "  %-16s FAIL\n" "$name"; rc=1; fi
done
[ $rc = 0 ] && echo "ALL PROVEN" || echo "FAILURES"
exit $rc
