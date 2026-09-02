#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/nonvacuity
python3 - <<'PY'
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location

path = Path("/tmp/audit-work/reconstruction/solution.py")
spec = spec_from_file_location("nonvacuity_solution", path)
assert spec is not None and spec.loader is not None
module = module_from_spec(spec)
spec.loader.exec_module(module)
actual = module.simplify("1/5", "5/1")
print(f"satisfying_witness=x=1/5,n=5/1,actual={actual},mutated_expected=False")
assert actual is True
PY

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition nonvacuity-kompiled

set +e
proof_output="$(kprove spec-vacuity.k \
  --definition nonvacuity-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.false-result-mutation 2>&1)"
proof_exit=$?
set -e
printf '%s\n' "$proof_output"
printf 'false_postcondition_kprove_exit=%s\n' "$proof_exit"
test "$proof_exit" -ne 0
grep -Fq 'WarnStuckClaimState' <<<"$proof_output"
grep -Fq "doesn't unify with the destination's term" <<<"$proof_output"
grep -Fq 'result ( boolVal ( true ) )' <<<"$proof_output"
