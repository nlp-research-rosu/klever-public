#!/usr/bin/env bash
set -u
set -o pipefail

scratch=/tmp/audit-work/5-intersperse
evidence=/audit-output/evidence
overall=0

run_logged() {
  local name="$1"
  shift
  local log="$evidence/$name"
  printf 'COMMAND'
  printf ' %q' "$@"
  printf '\nLOG %s\n' "$log"
  "$@" >"$log" 2>&1
  local status=$?
  printf 'EXIT %d\n' "$status"
  if [[ -s "$log" ]]; then
    printf 'OUTPUT_BEGIN\n'
    tail -n 140 "$log"
    printf 'OUTPUT_END\n'
  fi
  return "$status"
}

printf 'Constructor-level entry-program identity\n'
python3 "$evidence/04_extract_entry_module.py" "$scratch/spec.k" \
  > "$scratch/entry-claim-module.mpy"
extract_status=$?
printf 'extract_exit=%d\n' "$extract_status"
if [[ "$extract_status" -ne 0 ]]; then
  overall=1
fi

run_logged 04_kast_solution.log \
  kast "$scratch/solution.mpy" \
  --definition "$scratch/verification-kompiled" \
  --output kore
kast_solution_status=$?
if [[ "$kast_solution_status" -ne 0 ]]; then
  overall=1
fi

run_logged 04_kast_entry_module.log \
  kast "$scratch/entry-claim-module.mpy" \
  --definition "$scratch/verification-kompiled" \
  --output kore
kast_entry_status=$?
if [[ "$kast_entry_status" -ne 0 ]]; then
  overall=1
fi

if cmp -s "$evidence/04_kast_solution.log" "$evidence/04_kast_entry_module.log"; then
  printf 'constructor_identity=YES\n'
else
  printf 'constructor_identity=NO\n'
  overall=1
fi
sha256sum "$evidence/04_kast_solution.log" "$evidence/04_kast_entry_module.log"

printf 'Concrete satisfying entry witness against both Python implementations\n'
python3 - "$scratch/canonical.py" "$scratch/solution.py" <<'PY'
import importlib.util
import sys

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersperse

canonical = load("canonical_ground", sys.argv[1])
generated = load("generated_ground", sys.argv[2])
numbers = [1, 2, 3]
delimiter = 4
expected = [1, 4, 2, 4, 3]
print(f"precondition_witness numbers={numbers} delimiter={delimiter}")
print(f"trusted_canonical={canonical(numbers, delimiter)}")
print(f"generated_solution={generated(numbers, delimiter)}")
print(f"claimed_heap_list={expected}")
assert canonical(numbers, delimiter) == generated(numbers, delimiter) == expected
PY
python_status=$?
printf 'python_ground_exit=%d\n' "$python_status"
if [[ "$python_status" -ne 0 ]]; then
  overall=1
fi

cp "$evidence/04_ground_spec.k" "$scratch/04_ground_spec.k"
run_logged 04_kprove_ground.log \
  kprove "$scratch/04_ground_spec.k" \
  --definition "$scratch/verification-kompiled" \
  --spec-module AUDIT-GROUND-SPEC
ground_status=$?
if [[ "$ground_status" -ne 0 ]] || ! grep -Fxq '#Top' "$evidence/04_kprove_ground.log"; then
  overall=1
fi
printf 'ground_kprove_exit=%d exact_top=%s\n' \
  "$ground_status" \
  "$(if grep -Fxq '#Top' "$evidence/04_kprove_ground.log"; then printf YES; else printf NO; fi)"

cp "$evidence/04_body_mutation.k" "$scratch/04_body_mutation.k"
run_logged 04_kprove_body_mutation.log \
  kprove "$scratch/04_body_mutation.k" \
  --definition "$scratch/verification-kompiled" \
  --spec-module AUDIT-BODY-MUTATION
body_status=$?
if [[ "$body_status" -eq 0 ]] \
   || grep -Fxq '#Top' "$evidence/04_kprove_body_mutation.log" \
   || ! grep -q 'WarnStuckClaimState' "$evidence/04_kprove_body_mutation.log"; then
  overall=1
fi
printf 'body_mutation_kprove_exit=%d exact_top=%s stuck_claim=%s\n' \
  "$body_status" \
  "$(if grep -Fxq '#Top' "$evidence/04_kprove_body_mutation.log"; then printf YES; else printf NO; fi)" \
  "$(if grep -q 'WarnStuckClaimState' "$evidence/04_kprove_body_mutation.log"; then printf YES; else printf NO; fi)"

printf 'ADEQUACY_SCRIPT_STATUS=%d\n' "$overall"
exit "$overall"
