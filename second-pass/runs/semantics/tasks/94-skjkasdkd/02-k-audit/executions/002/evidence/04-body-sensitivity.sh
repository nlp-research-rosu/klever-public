#!/usr/bin/env bash
set -u

evidence=/audit-output/evidence
work=/tmp/audit-work/body-mutation
overall=0

run_logged() {
  local name="$1"
  shift
  local log="$evidence/$name.log"
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    rc=$?
    echo "EXIT_STATUS=$rc"
  } > "$log" 2>&1
  echo "$name exit=$rc"
  return "$rc"
}

{
  echo "COMMAND: translate the materially changed body and its concrete probe"
  python3 py2mpy.py solution-body-mut.py > solution-body-mut.mpy
  first_rc=$?
  python3 py2mpy.py body-mut-concrete.py > body-mut-concrete.mpy
  second_rc=$?
  echo "solution_translate_status=$first_rc"
  echo "concrete_translate_status=$second_rc"
} > "$evidence/04-body-mut-translate.log" 2>&1
(( first_rc == 0 && second_rc == 0 )) || overall=1

run_logged 04-body-mut-kompile-bridge \
  kompile verification-body-mut.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition body-mut-bridge-kompiled \
  -I . || overall=1

run_logged 04-body-mut-kompile-no-bridge \
  kompile verification-body-mut-no-bridge.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition body-mut-no-bridge-kompiled \
  -I . || overall=1

{
  echo "COMMAND: kast changed solution body and changed solutionModule"
  kast --definition body-mut-bridge-kompiled --module VERIFICATION \
    --sort Module --expand-macros --output kore \
    solution-body-mut.mpy --output-file solution-body-mut.kore
  body_rc=$?
  kast --definition body-mut-bridge-kompiled --module VERIFICATION \
    --sort Module --expand-macros --output kore \
    solution-module-symbol.mpy --output-file solution-module-body-mut.kore
  symbol_rc=$?
  cmp solution-body-mut.kore solution-module-body-mut.kore
  cmp_rc=$?
  sha256sum solution-body-mut.kore solution-module-body-mut.kore
  echo "body_kast_status=$body_rc"
  echo "symbol_kast_status=$symbol_rc"
  echo "changed_constructor_cmp_status=$cmp_rc"
} > "$evidence/04-body-mut-kast-pin.log" 2>&1
(( body_rc == 0 && symbol_rc == 0 && cmp_rc == 0 )) || overall=1

run_logged 04-body-mut-concrete-krun \
  krun body-mut-concrete.mpy \
  --definition /tmp/audit-work/reconstruction/reviewer-runtime-kompiled \
  || overall=1

run_logged 04-body-mut-ground-with-bridge \
  kprove body-mut-ground-bridge.k \
  --definition body-mut-bridge-kompiled \
  --spec-module BODY-MUT-GROUND-BRIDGE \
  --output pretty || overall=1

run_logged 04-body-mut-full-main-with-bridge \
  kprove spec-body-mut.k \
  --definition body-mut-bridge-kompiled \
  --spec-module SPEC \
  --claims SPEC.main-correct,SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --trusted SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --output pretty || overall=1

run_logged 04-body-mut-ground-without-bridge \
  kprove body-mut-ground-no-bridge.k \
  --definition body-mut-no-bridge-kompiled \
  --spec-module BODY-MUT-GROUND-NO-BRIDGE \
  --output pretty
no_bridge_rc=$?
if (( no_bridge_rc == 0 )); then
  echo "unexpected: false fixed-semantics mutation closed"
  overall=1
elif rg -q 'WarnStuckClaimState|cannot be rewritten further' \
  "$evidence/04-body-mut-ground-without-bridge.log" \
  && rg -q '<k>|1' "$evidence/04-body-mut-ground-without-bridge.log"; then
  echo "expected: bridge-free fixed execution rejects result 2"
else
  echo "unexpected failure mode in bridge-free probe"
  overall=1
fi

{
  echo "COMMAND: Python ground comparison on intended input [2]"
  python3 -c '
import importlib.util
from pathlib import Path
def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.skjkasdkd
print("mutated_body", load(Path("solution-body-mut.py"))([2]))
print("immutable_candidate", load(Path("/tmp/audit-work/reconstruction/solution.py"))([2]))
print("trusted_canonical", load(Path("/tmp/audit-work/reconstruction/canonical.py"))([2]))
'
  rc=$?
  echo "EXIT_STATUS=$rc"
} > "$evidence/04-body-mut-python.log" 2>&1
(( rc == 0 )) || overall=1

for log in \
  "$evidence/04-body-mut-ground-with-bridge.log" \
  "$evidence/04-body-mut-full-main-with-bridge.log"; do
  if ! grep -Fxq '#Top' "$log" || ! grep -Fxq 'EXIT_STATUS=0' "$log"; then
    overall=1
  fi
done

echo "FINAL_STATUS=$overall"
exit "$overall"
