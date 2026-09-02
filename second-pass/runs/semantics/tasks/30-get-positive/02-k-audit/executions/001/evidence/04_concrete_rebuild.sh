#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive
failed=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    failed=1
  fi
}

printf '$ python3 /reference/py2mpy.py /audit-output/evidence/04_reviewer_concrete.py > %s/reviewer-concrete.mpy\n' "$work"
python3 /reference/py2mpy.py \
  /audit-output/evidence/04_reviewer_concrete.py \
  > "$work/reviewer-concrete.mpy"
status=$?
printf '[exit %d]\n' "$status"
if test "$status" -ne 0; then
  failed=1
fi

run kompile "$work/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/runtime-kompiled"

run krun "$work/solution.mpy" \
  --definition "$work/runtime-kompiled"

run python3 /audit-output/evidence/04_reviewer_concrete.py

run krun "$work/reviewer-concrete.mpy" \
  --definition "$work/runtime-kompiled"

exit "$failed"

