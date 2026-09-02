#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

printf '%s  %s\n' \
  f1320cc5aa8f242a9ad1695acd5a0f3d12c0033053d911a8bd4f7ebae6b3848c \
  solution.mpy | sha256sum -c -

python3 - <<'PY'
import ast

def target_function(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    return next(node for node in tree.body
                if isinstance(node, ast.FunctionDef)
                and node.name == "parse_nested_parens")

solution_function = target_function("solution.py")
smoke_function = target_function("smoke.py")
assert ast.dump(solution_function, include_attributes=False) == ast.dump(
    smoke_function, include_attributes=False
)
print("smoke function AST matches solution.py")
PY

python3 test_differential.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled | tee concrete-run.log
grep -q '<k>' concrete-run.log
grep -q '    .K' concrete-run.log
grep -q '    NoExc' concrete-run.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee positive-proof.log
grep -qx '#Top' positive-proof.log

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY > vacuity-probe.log 2>&1; then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  vacuity_status=$?
fi
grep -q 'WarnStuckClaimState' vacuity-probe.log
grep -q 'list ( vCons ( 1 , .ValSeq ) )' vacuity-probe.log
echo "false-result mutation: expected failure (exit ${vacuity_status})"

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION > body-mutation-probe.log 2>&1; then
  echo "ERROR: mutated body unexpectedly proved" >&2
  exit 1
else
  body_status=$?
fi
grep -q 'WarnStuckClaimState' body-mutation-probe.log
grep -q 'list ( vCons ( 2 , .ValSeq ) )' body-mutation-probe.log
echo "body mutation: expected failure (exit ${body_status})"
