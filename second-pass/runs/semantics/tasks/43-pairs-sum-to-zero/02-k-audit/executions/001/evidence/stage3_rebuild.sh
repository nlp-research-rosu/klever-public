#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/pairs-audit
EVIDENCE=/audit-output/evidence
cd "$WORK" || exit 99
export PATH="$HOME/.nix-profile/bin:$PATH"

run_logged() {
  local name="$1"
  shift
  local logfile="$EVIDENCE/$name.log"
  (
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    status=$?
    printf 'exit=%s\n' "$status"
    exit "$status"
  ) >"$logfile" 2>&1
  local status=$?
  printf '%s exit=%s log=%s\n' "$name" "$status" "$logfile"
  return "$status"
}

overall=0

run_logged stage3_translate_concrete \
  python3 trusted-py2mpy.py concrete-tests.py
status=$?
if (( status == 0 )); then
  python3 trusted-py2mpy.py concrete-tests.py > regenerated-concrete-tests.mpy
  cmp regenerated-concrete-tests.mpy concrete-tests.mpy
  status=$?
  {
    echo '$ cmp regenerated-concrete-tests.mpy concrete-tests.mpy'
    echo "exit=$status"
    sha256sum regenerated-concrete-tests.mpy concrete-tests.mpy
  } >> "$EVIDENCE/stage3_translate_concrete.log"
fi
(( status == 0 )) || overall=1

run_logged stage3_kompile_llvm \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
status=$?
(( status == 0 )) || overall=1

if (( status == 0 )); then
  run_logged stage3_krun_concrete \
    krun regenerated-concrete-tests.mpy \
    --definition runtime-kompiled
  status=$?
  (( status == 0 )) || overall=1
fi

run_logged stage3_kompile_base \
  kompile verification.k \
  --backend haskell \
  --main-module PAIRS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
base_status=$?
(( base_status == 0 )) || overall=1

if (( base_status == 0 )); then
  for claim in bounded-empty bounded-one bounded-two membership-summary; do
    run_logged "stage3_kprove_${claim}" \
      kprove spec.k \
      --definition verification-kompiled \
      --spec-module PAIRS-SUMMARY-SPEC \
      --claims "PAIRS-SUMMARY-SPEC.$claim"
    status=$?
    (( status == 0 )) || overall=1
  done

  run_logged stage3_kprove_loop-summary \
    kprove spec.k \
    --definition verification-kompiled \
    --spec-module PAIRS-SUMMARY-SPEC \
    --claims PAIRS-SUMMARY-SPEC.membership-summary,PAIRS-SUMMARY-SPEC.loop-summary \
    --trusted PAIRS-SUMMARY-SPEC.membership-summary
  status=$?
  (( status == 0 )) || overall=1
fi

run_logged stage3_kompile_lemmas \
  kompile verification.k \
  --backend haskell \
  --main-module PAIRS-VERIFICATION-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-lemmas-kompiled
lemmas_status=$?
(( lemmas_status == 0 )) || overall=1

if (( lemmas_status == 0 )); then
  run_logged stage3_kprove_all-integer-lists \
    kprove spec.k \
    --definition verification-lemmas-kompiled \
    --spec-module PAIRS-MAIN-SPEC \
    --claims PAIRS-MAIN-SPEC.all-integer-lists
  status=$?
  (( status == 0 )) || overall=1
fi

exit "$overall"
