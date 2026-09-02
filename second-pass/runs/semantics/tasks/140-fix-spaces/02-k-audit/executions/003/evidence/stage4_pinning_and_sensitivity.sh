#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/140-fix-spaces/source
cd "$scratch" || exit 90
failures=0

run_command() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'exit=%s\n' "$status"
  return "$status"
}

echo '$ parse and fully macro-expand the proof term solutionModule'
kast \
  --definition fresh-proof-main-kompiled \
  --module FIX-SPACES-VERIFICATION \
  --sort Module \
  --expand-macros \
  --output json \
  --output-file /audit-output/evidence/program_from_claim_macro.json \
  --expression solutionModule
macro_status=$?
echo "exit=$macro_status"

echo '$ parse and fully macro-expand the regenerated submitted solution.mpy'
kast \
  --definition fresh-proof-main-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --expand-macros \
  --output json \
  --output-file /audit-output/evidence/program_from_submitted_mpy.json \
  regenerated-solution.mpy
submitted_status=$?
echo "exit=$submitted_status"

run_command cmp \
  /audit-output/evidence/program_from_claim_macro.json \
  /audit-output/evidence/program_from_submitted_mpy.json
compare_status=$?
run_command sha256sum \
  /audit-output/evidence/program_from_claim_macro.json \
  /audit-output/evidence/program_from_submitted_mpy.json

echo '$ prove the ground substitution of the claimed result for input a followed by two spaces'
kprove ground-result-spec.k \
  --definition fresh-proof-base-kompiled \
  --spec-module GROUND-RESULT-SPEC
ground_status=$?
echo "exit=$ground_status"

echo '$ evaluate both Python entry points and the prose oracle on the same satisfying input'
python3 - <<'PY'
import importlib.util

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fix_spaces

canonical = load("canonical.py", "canonical_witness")
candidate = load("solution.py", "candidate_witness")
text = "a  "
print("input=", repr(text))
print("candidate=", repr(candidate(text)))
print("canonical=", repr(canonical(text)))
print("formal_ground_codes=", [97, 95, 95])
PY
python_status=$?
echo "exit=$python_status"

echo '$ show the one material body mutation'
diff -u verification.k verification-body-mutated.k
diff_status=$?
echo "exit=$diff_status (1 means files differ as intended)"

echo '$ build a fresh definition whose actually executed function body has the mutation'
kompile verification-body-mutated.k \
  --backend haskell \
  --main-module FIX-SPACES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-body-mutated-kompiled
build_mutation_status=$?
echo "exit=$build_mutation_status"

echo '$ require the unchanged result summary to be rejected for the mutated executed body'
kprove spec-body-mutated.k \
  --definition fresh-body-mutated-kompiled \
  --spec-module FIX-SPACES-BODY-MUTATED-SPEC
proof_mutation_status=$?
echo "exit=$proof_mutation_status (nonzero expected)"

if [ "$macro_status" -ne 0 ] ||
   [ "$submitted_status" -ne 0 ] ||
   [ "$compare_status" -ne 0 ] ||
   [ "$ground_status" -ne 0 ] ||
   [ "$python_status" -ne 0 ] ||
   [ "$diff_status" -ne 1 ] ||
   [ "$build_mutation_status" -ne 0 ] ||
   [ "$proof_mutation_status" -eq 0 ]; then
  failures=1
fi

echo "audit_check_failures=$failures"
exit "$failures"
