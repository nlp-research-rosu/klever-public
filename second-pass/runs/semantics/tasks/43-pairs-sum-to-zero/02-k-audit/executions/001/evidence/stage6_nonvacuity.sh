#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/pairs-audit
EVIDENCE=/audit-output/evidence
SPEC=/audit-output/evidence/stage6_false-mutation.k
cd "$WORK" || exit 99
export PATH="$HOME/.nix-profile/bin:$PATH"

(
  echo "$ kprove $SPEC --definition verification-lemmas-kompiled --spec-module AUDIT-FALSE-MUTATION --claims AUDIT-FALSE-MUTATION.negated-result --dry-run"
  kprove "$SPEC" \
    --definition verification-lemmas-kompiled \
    --spec-module AUDIT-FALSE-MUTATION \
    --claims AUDIT-FALSE-MUTATION.negated-result \
    --dry-run
  status=$?
  echo "exit=$status"
  exit "$status"
) > "$EVIDENCE/stage6_mutation_dry_run.log" 2>&1
dry_status=$?
echo "mutation_dry_run_exit=$dry_status"

(
  echo "$ kprove $SPEC --definition verification-lemmas-kompiled --spec-module AUDIT-FALSE-MUTATION --claims AUDIT-FALSE-MUTATION.negated-result"
  kprove "$SPEC" \
    --definition verification-lemmas-kompiled \
    --spec-module AUDIT-FALSE-MUTATION \
    --claims AUDIT-FALSE-MUTATION.negated-result
  status=$?
  echo "exit=$status"
  exit "$status"
) > "$EVIDENCE/stage6_mutation_proof.log" 2>&1
proof_status=$?
echo "mutation_proof_exit=$proof_status"

python3 - <<'PY'
import importlib.util

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pairs_sum_to_zero

values = [0, 0]
canonical = load("/reference/canonical.py", "canonical_mutation")(values)
generated = load(
    "/tmp/audit-work/pairs-audit/solution.py", "generated_mutation"
)(values)
formal_pairs_is = True
mutated_target = not formal_pairs_is
print(
    f"satisfying_input={values!r} canonical={canonical} "
    f"generated={generated} formal_pairsIS={formal_pairs_is} "
    f"mutated_target={mutated_target}"
)
if not (canonical is generated is formal_pairs_is is True):
    raise SystemExit(1)
PY
witness_status=$?
echo "mutation_witness_exit=$witness_status"

if (( dry_status != 0 || proof_status == 0 || witness_status != 0 )); then
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$EVIDENCE/stage6_mutation_proof.log"; then
  echo 'missing expected WarnStuckClaimState residual'
  exit 1
fi
exit 0
