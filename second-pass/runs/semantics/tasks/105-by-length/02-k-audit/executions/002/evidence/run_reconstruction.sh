#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/105-by-length/recon
overall=0

if [[ -e "$scratch/runtime-kompiled" || -e "$scratch/verification-kompiled" ]]; then
  printf 'ERROR: compiled definition unexpectedly existed before reconstruction\n'
  exit 90
fi
printf 'CLEAN_START: no compiled definitions present\n'

printf 'COMMAND: cd %s && kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled\n' "$scratch"
(
  cd "$scratch" || exit 90
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-kompiled
)
llvm_rc=$?
printf 'LLVM_KOMPILE_EXIT_STATUS: %s\n' "$llvm_rc"
if (( llvm_rc != 0 )); then
  overall=1
fi

printf 'COMMAND: python3 /audit-output/evidence/make_k_concrete_tests.py\n'
python3 /audit-output/evidence/make_k_concrete_tests.py
generator_rc=$?
printf 'CONCRETE_GENERATOR_EXIT_STATUS: %s\n' "$generator_rc"
if (( generator_rc != 0 )); then
  overall=1
fi

if (( llvm_rc == 0 && generator_rc == 0 )); then
  printf 'COMMAND: cd %s && krun audit-concrete.mpy --definition runtime-kompiled --output none\n' "$scratch"
  (
    cd "$scratch" || exit 90
    krun audit-concrete.mpy \
      --definition runtime-kompiled \
      --output none
  )
  krun_rc=$?
else
  krun_rc=99
fi
printf 'KRUN_EXIT_STATUS: %s\n' "$krun_rc"
if (( krun_rc != 0 )); then
  overall=1
fi

printf 'COMMAND: cd %s && kompile verification.k --backend haskell --main-module BY-LENGTH-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled\n' "$scratch"
(
  cd "$scratch" || exit 90
  kompile verification.k \
    --backend haskell \
    --main-module BY-LENGTH-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-kompiled
)
haskell_rc=$?
printf 'HASKELL_KOMPILE_EXIT_STATUS: %s\n' "$haskell_rc"
if (( haskell_rc != 0 )); then
  overall=1
fi

if (( haskell_rc == 0 )); then
  printf 'COMMAND: cd %s && kprove spec.k --definition verification-kompiled --spec-module BY-LENGTH-SPEC\n' "$scratch"
  (
    cd "$scratch" || exit 90
    set -o pipefail
    kprove spec.k \
      --definition verification-kompiled \
      --spec-module BY-LENGTH-SPEC \
      2>&1 | tee positive-kprove.stdout
  )
  kprove_rc=$?
  if rg -x '#Top' "$scratch/positive-kprove.stdout" >/dev/null; then
    top_rc=0
  else
    top_rc=1
  fi
else
  kprove_rc=99
  top_rc=99
fi
printf 'KPROVE_EXIT_STATUS: %s\n' "$kprove_rc"
printf 'KPROVE_TOP_CHECK_EXIT_STATUS: %s\n' "$top_rc"
if (( kprove_rc != 0 || top_rc != 0 )); then
  overall=1
fi

printf 'EXIT_STATUS: %s\n' "$overall"
exit "$overall"
