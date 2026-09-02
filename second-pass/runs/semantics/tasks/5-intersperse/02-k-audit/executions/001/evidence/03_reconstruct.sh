#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

SCRATCH=/tmp/audit-work/candidate
printf '%s\n' 'Stage 3: clean proof reconstruction'
printf 'scratch=%s\n' "$SCRATCH"

run find "$SCRATCH" -maxdepth 2 -type d -name '*-kompiled' -o -name '.kompile-*'
run sha256sum "$SCRATCH/solution.py" "$SCRATCH/solution.mpy" \
  "$SCRATCH/spec.k" "$SCRATCH/verification.k"

run python3 /reference/py2mpy.py /audit-output/evidence/03_concrete_program.py
python3 /reference/py2mpy.py /audit-output/evidence/03_concrete_program.py \
  > "$SCRATCH/audit-concrete.mpy"
printf '\n$ python3 /reference/py2mpy.py /audit-output/evidence/03_concrete_program.py > %s/audit-concrete.mpy\n' "$SCRATCH"
printf '[exit %d]\n' "$?"

run kompile "$SCRATCH/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/runtime-kompiled"

run krun "$SCRATCH/audit-concrete.mpy" \
  --definition "$SCRATCH/runtime-kompiled"

run kompile "$SCRATCH/verification.k" \
  --backend haskell \
  --main-module INTERSPERSE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/verification-kompiled"

run kprove "$SCRATCH/spec.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module INTERSPERSE-SPEC
