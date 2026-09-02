#!/usr/bin/env bash
# Re-verify EVERY checked (converted) pass-0 problem against the CURRENT reference
# semantics: re-kompile each verification.k (haskell) and re-kprove each spec.k, memory-
# capped. Run this after any change to reference/src/ (auto mode step 2d). Also re-runs
# the reference's own proof tests. Prints a PASS/FAIL line per problem; exits non-zero if
# any regressed. Usage: bash scripts/reverify-all.sh [--kompile-llvm]
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HE="$ROOT/verification/humaneval"
Q="$HE/questions"
CAP=(systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 --quiet timeout 500)

if [ "${1:-}" = "--kompile-llvm" ]; then
  echo "== re-kompile reference LLVM =="
  kompile "$HE/reference/src/semantics.k" --backend llvm --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX --output-definition "$HE/reference/src/semantics-kompiled" \
    >/dev/null 2>&1 && echo "  llvm OK" || { echo "  llvm KOMPILE-FAIL"; exit 1; }
fi

rc=0
# ticked folders, in PROVEN.md order
mapfile -t FOLDERS < <(grep -oE '^\| \[x\] \|.*\(questions/[^/]+/' "$HE/PROVEN.md" | grep -oE 'questions/[^/]+/' | sed 's#questions/##; s#/##')
echo "== ${#FOLDERS[@]} checked problems =="
for f in "${FOLDERS[@]}"; do
  d="$Q/$f"
  [ -f "$d/verification.k" ] || { printf "  %-30s NO-VERIFICATION\n" "$f"; rc=1; continue; }
  VMOD="$(grep -oE 'module [A-Z0-9-]+-VERIFICATION' "$d/verification.k" | head -1 | awk '{print $2}')"
  SMOD="$(grep -oE 'module [A-Z0-9-]+-SPEC' "$d/spec.k" | head -1 | awk '{print $2}')"
  if ! kompile "$d/verification.k" --backend haskell --main-module "$VMOD" \
        --syntax-module MPY-SYNTAX --output-definition "$d/verification-kompiled" >/dev/null 2>&1; then
    printf "  %-30s KOMPILE-FAIL\n" "$f"; rc=1; continue
  fi
  out="$("${CAP[@]}" kprove "$d/spec.k" --definition "$d/verification-kompiled" --spec-module "$SMOD" 2>&1)"
  if printf '%s' "$out" | grep -q '^#Top'; then printf "  %-30s #Top\n" "$f"
  else printf "  %-30s FAIL\n" "$f"; rc=1; fi
done
echo "== reference proof tests =="
bash "$HE/reference/tests/verify.sh" 2>&1 | sed 's/^/  /'
[ $rc = 0 ] && echo "ALL CHECKED PROBLEMS #Top" || echo "REGRESSIONS DETECTED"
exit $rc
