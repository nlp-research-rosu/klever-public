#!/usr/bin/env bash
set +e
scratch=/tmp/audit-work/92-any-int-audit
evidence=/audit-output/evidence

printf '$ find -P /tmp/audit-work/92-any-int-audit -maxdepth 1 -name "*-kompiled" -print\n'
find -P "$scratch" -maxdepth 1 -name '*-kompiled' -print
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf '$ python3 /audit-output/evidence/03_concrete_audit.py\n'
python3 "$evidence/03_concrete_audit.py"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

printf '$ python3 /reference/py2mpy.py /audit-output/evidence/03_concrete_audit.py > /tmp/audit-work/92-any-int-audit/03_concrete_audit.mpy\n'
python3 /reference/py2mpy.py "$evidence/03_concrete_audit.py" > "$scratch/03_concrete_audit.mpy"
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

printf '$ kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled\n'
(
  cd "$scratch" || exit 125
  kompile --backend llvm reference-semantics/semantics.k \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled
) > "$evidence/03_kompile_llvm.log" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
tail -n 120 "$evidence/03_kompile_llvm.log"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

printf '$ krun 03_concrete_audit.mpy --definition audit-runtime-kompiled\n'
(
  cd "$scratch" || exit 125
  krun 03_concrete_audit.mpy --definition audit-runtime-kompiled
) > "$evidence/03_krun.log" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
tail -n 160 "$evidence/03_krun.log"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

printf '$ kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled\n'
(
  cd "$scratch" || exit 125
  kompile --backend haskell verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-kompiled
) > "$evidence/03_kompile_haskell.log" 2>&1
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
tail -n 160 "$evidence/03_kompile_haskell.log"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

claims=(
  int-int-int
  int-int-bool
  int-bool-int
  int-bool-bool
  bool-int-int
  bool-int-bool
  bool-bool-int
  bool-bool-bool
  float-any-any
  int-float-any
  bool-float-any
  int-int-float
  int-bool-float
  bool-int-float
  bool-bool-float
)

proof_failures=0
for label in "${claims[@]}"; do
  log="$evidence/03_kprove_${label}.log"
  printf '$ kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.%s\n' "$label"
  (
    cd "$scratch" || exit 125
    kprove spec.k \
      --definition audit-verification-kompiled \
      --spec-module SPEC \
      --claims "SPEC.${label}"
  ) > "$log" 2>&1
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  tail -n 120 "$log"
  if [ "$status" -ne 0 ] || ! grep -Fxq '#Top' "$log"; then
    proof_failures=$((proof_failures + 1))
  fi
done

printf 'POSITIVE_CLAIM_SUMMARY: total=%d failures=%d\n' "${#claims[@]}" "$proof_failures"
exit "$proof_failures"
