#!/usr/bin/env bash
set -euo pipefail

# Regenerate the translated program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy

# Build the required concrete LLVM definition.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

# Add one top-level assignment to a temporary concrete harness. The final
# character removed here is solution.mpy's closing Module parenthesis.
sed '$s/.$//' solution.mpy > concrete-test.mpy
printf '  Assign(Name("answer"), Call(Name("prime_fib"), Int(11)))\n)\n' \
  >> concrete-test.mpy
krun concrete-test.mpy --definition runtime-kompiled | tee krun.out
grep -F '"answer" |-> 2971215073' krun.out

# Build the symbolic definition, importing MPY (not MPY-CONCRETE).
kompile verification.k \
  --backend haskell \
  --main-module PRIME-FIB-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled

# The eleven independent claims are balanced across three proof processes.
# Peak use remains below the container's 8 GB limit, while every kprove
# command still proves only claims from spec.k and must print #Top.
run_group() {
  local claims=$1
  local log=$2
  kprove spec.k \
    --definition proof-kompiled \
    --spec-module PRIME-FIB-SPEC \
    --claims "$claims" 2>&1 | tee "$log"
}

run_group \
  PRIME-FIB-SPEC.pf11,PRIME-FIB-SPEC.pf4,PRIME-FIB-SPEC.pf3,PRIME-FIB-SPEC.pf2,PRIME-FIB-SPEC.pf1 \
  kprove-group-1.out &
group1=$!
run_group \
  PRIME-FIB-SPEC.pf10,PRIME-FIB-SPEC.pf7,PRIME-FIB-SPEC.pf5 \
  kprove-group-2.out &
group2=$!
run_group \
  PRIME-FIB-SPEC.pf9,PRIME-FIB-SPEC.pf8,PRIME-FIB-SPEC.pf6 \
  kprove-group-3.out &
group3=$!

wait "$group1"
wait "$group2"
wait "$group3"

grep -x '#Top' kprove-group-1.out
grep -x '#Top' kprove-group-2.out
grep -x '#Top' kprove-group-3.out
