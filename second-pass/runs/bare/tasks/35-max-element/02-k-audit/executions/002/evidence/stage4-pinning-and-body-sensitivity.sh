#!/usr/bin/env bash
set -euo pipefail
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
cd /tmp/audit-work/35-max-element

python3 /audit-output/evidence/program_term_compare.py

echo "SATISFYING_ENTRY_WITNESS=[2, -5, 2]"
python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element

canonical = load("stage4_canonical", "/reference/canonical.py")
candidate = load("stage4_candidate", "/tmp/audit-work/35-max-element/solution.py")
witness = [2, -5, 2]
print(f"CANONICAL_WITNESS_RESULT={canonical(witness.copy())}")
print(f"CANDIDATE_WITNESS_RESULT={candidate(witness.copy())}")
PY
krun solution.mpy \
  --definition audit-semantic-kompiled \
  --color off \
  -cARGS='[2, -5, 2]'

test ! -e audit-body-mutated-kompiled
kompile verification-body-mutated.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-body-mutated-kompiled

set +e
kprove spec-body-mutated.k \
  --definition audit-body-mutated-kompiled \
  --spec-module SPEC-BODY-MUTATED \
  > /audit-output/evidence/stage4-body-mutation-kprove.raw.log 2>&1
body_mutation_status=$?
set -e
echo "BODY_MUTATION_KPROVE_EXIT=$body_mutation_status"
sed -n '1,220p' /audit-output/evidence/stage4-body-mutation-kprove.raw.log
test "$body_mutation_status" -ne 0
rg -n 'WarnStuckClaimState|cannot be rewritten further' \
  /audit-output/evidence/stage4-body-mutation-kprove.raw.log
