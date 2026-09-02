#!/usr/bin/env bash
set -uo pipefail
set -x

scratch=/tmp/audit-work/candidate-src
raw=/tmp/audit-work/stage3-raw
mkdir -p "$raw"
overall=0

run_bounded() {
  local name=$1
  shift
  printf 'COMMAND[%s]:' "$name"
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$raw/$name.log" 2>&1
  local status=$?
  printf 'EXIT[%s]=%s\n' "$name" "$status"
  printf 'OUTPUT-BEGIN[%s]\n' "$name"
  sed -n '1,180p' "$raw/$name.log"
  local lines
  lines=$(wc -l < "$raw/$name.log")
  if (( lines > 220 )); then
    printf '... omitted_middle_lines=%s ...\n' "$((lines - 220))"
    tail -n 40 "$raw/$name.log"
  fi
  printf 'OUTPUT-END[%s]\n' "$name"
  if (( status != 0 )); then
    overall=1
  fi
  return 0
}

python3 - "$scratch/solution.py" "$scratch/concrete_driver.py" <<'PY'
from pathlib import Path
import sys

solution = Path(sys.argv[1]).read_text()
driver = Path(sys.argv[2]).read_text()
print(f"concrete_driver_exact_solution_prefix={driver.startswith(solution)}")
if not driver.startswith(solution):
    raise SystemExit(1)
PY
prefix_status=$?
printf 'concrete_driver_prefix_status=%s\n' "$prefix_status"
if (( prefix_status != 0 )); then
  overall=1
fi

run_bounded translate-concrete \
  python3 "$scratch/trusted-py2mpy.py" "$scratch/concrete_driver.py"
if (( overall == 0 )); then
  python3 "$scratch/trusted-py2mpy.py" "$scratch/concrete_driver.py" \
    > "$scratch/concrete_driver.mpy"
  printf 'WRITE[concrete-driver-mpy]=%s\n' "$?"
fi

run_bounded kompile-llvm \
  kompile "$scratch/reference-semantics/semantics.k" \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition "$scratch/audit-runtime-kompiled"

run_bounded krun-concrete \
  krun "$scratch/concrete_driver.mpy" \
    --definition "$scratch/audit-runtime-kompiled"

run_bounded kompile-base \
  kompile --backend haskell "$scratch/verification.k" \
    --main-module VERIFICATION-BASE \
    --syntax-module MPY-SYNTAX \
    --output-definition "$scratch/audit-verification-base-kompiled"

run_bounded kprove-loop \
  kprove "$scratch/spec.k" \
    --definition "$scratch/audit-verification-base-kompiled" \
    --spec-module LOOP-SPEC
grep -Fx '#Top' "$raw/kprove-loop.log"
loop_top_status=$?
printf 'TOP-CHECK[kprove-loop]=%s\n' "$loop_top_status"
if (( loop_top_status != 0 )); then
  overall=1
fi

run_bounded kompile-full \
  kompile --backend haskell "$scratch/verification.k" \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$scratch/audit-verification-kompiled"

run_bounded kprove-entry \
  kprove "$scratch/spec.k" \
    --definition "$scratch/audit-verification-kompiled" \
    --spec-module SPEC
grep -Fx '#Top' "$raw/kprove-entry.log"
entry_top_status=$?
printf 'TOP-CHECK[kprove-entry]=%s\n' "$entry_top_status"
if (( entry_top_status != 0 )); then
  overall=1
fi

printf 'STAGE3_OVERALL=%s\n' "$overall"
exit "$overall"
