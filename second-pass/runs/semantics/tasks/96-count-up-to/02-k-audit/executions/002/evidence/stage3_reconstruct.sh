#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/audit96
build="$scratch/build"
evidence=/audit-output/evidence
mkdir -p "$build"

run_logged() {
  local label=$1
  shift
  local rendered
  printf -v rendered '%q ' "$@"
  printf 'COMMAND[%s]: %s\n' "$label" "$rendered"
  script -q -e -c "$rendered" "$evidence/$label.log"
  local status=$?
  printf 'EXIT[%s]: %s\n' "$label" "$status"
  return "$status"
}

overall=0

run_logged stage3_versions bash -lc \
  'kompile --version && kprove --version && krun --version' || overall=1

cp "$scratch/solution.py" "$build/concrete_tests.py"
sed -n '/^assert /,$p' "$scratch/concrete_assertions.py" \
  >> "$build/concrete_tests.py"
run_logged stage3_translate_concrete python3 "$scratch/py2mpy.py" \
  "$build/concrete_tests.py" || overall=1
# The translator writes its MPY term to stdout, so preserve a clean generated
# term separately from the command transcript.
python3 "$scratch/py2mpy.py" "$build/concrete_tests.py" \
  > "$build/concrete_tests.mpy"
translate_status=$?
printf 'EXIT[stage3_translate_concrete_file]: %s\n' "$translate_status"
if (( translate_status != 0 )); then overall=1; fi

run_logged stage3_build_llvm kompile \
  "$scratch/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build/runtime-kompiled" || overall=1

run_logged stage3_krun_examples krun "$build/concrete_tests.mpy" \
  --definition "$build/runtime-kompiled" \
  --output pretty || overall=1

run_logged stage3_build_inner kompile "$scratch/verification.k" \
  --backend haskell \
  --main-module COUNT-UP-TO-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build/inner-proof-kompiled" || overall=1

run_logged stage3_prove_inner kprove "$scratch/spec.k" \
  --definition "$build/inner-proof-kompiled" \
  --spec-module COUNT-UP-TO-INNER-LOOP-SPEC || overall=1

run_logged stage3_build_outer kompile "$scratch/verification.k" \
  --backend haskell \
  --main-module COUNT-UP-TO-WITH-INNER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build/outer-proof-kompiled" || overall=1

run_logged stage3_prove_outer kprove "$scratch/spec.k" \
  --definition "$build/outer-proof-kompiled" \
  --spec-module COUNT-UP-TO-OUTER-LOOP-SPEC || overall=1

run_logged stage3_build_entry kompile "$scratch/verification.k" \
  --backend haskell \
  --main-module COUNT-UP-TO-WITH-OUTER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build/entry-proof-kompiled" || overall=1

run_logged stage3_prove_entry kprove "$scratch/spec.k" \
  --definition "$build/entry-proof-kompiled" \
  --spec-module COUNT-UP-TO-ENTRY-SPEC || overall=1

run_logged stage3_prove_boundary kprove "$scratch/spec.k" \
  --definition "$build/entry-proof-kompiled" \
  --spec-module COUNT-UP-TO-BOUNDARY-SPEC || overall=1

printf 'OVERALL_STAGE3_RECONSTRUCTION=%s\n' "$overall"
exit "$overall"
