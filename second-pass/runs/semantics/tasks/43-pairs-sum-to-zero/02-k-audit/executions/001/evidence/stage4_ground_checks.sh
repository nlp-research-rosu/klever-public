#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/pairs-audit
EVIDENCE=/audit-output/evidence
SPEC=/audit-output/evidence/stage4_ground-spec.k
cd "$WORK" || exit 99
export PATH="$HOME/.nix-profile/bin:$PATH"

claims=(
  real-empty
  real-single-zero
  real-double-zero
  real-late-pair
  real-no-pair
  formal-empty
  formal-single-zero
  formal-double-zero
  formal-late-pair
  formal-no-pair
)

overall=0
for claim in "${claims[@]}"; do
  logfile="$EVIDENCE/stage4_kprove_${claim}.log"
  (
    echo "$ kprove $SPEC --definition verification-kompiled --spec-module AUDIT-GROUND-SPEC --claims AUDIT-GROUND-SPEC.$claim"
    kprove "$SPEC" \
      --definition verification-kompiled \
      --spec-module AUDIT-GROUND-SPEC \
      --claims "AUDIT-GROUND-SPEC.$claim"
    status=$?
    echo "exit=$status"
    exit "$status"
  ) >"$logfile" 2>&1
  status=$?
  echo "stage4_kprove_${claim} exit=$status log=$logfile"
  (( status == 0 )) || overall=1
done

echo '$ Python substitutions against trusted canonical and generated entry points'
python3 - <<'PY'
import importlib.util

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pairs_sum_to_zero

canonical = load("/reference/canonical.py", "canonical_ground")
generated = load("/tmp/audit-work/pairs-audit/solution.py", "generated_ground")
cases = [
    ([], False),
    ([0], False),
    ([0, 0], True),
    ([2, 4, -5, 3, 5, 7], True),
    ([1, 3, -2, 1], False),
]
for values, expected in cases:
    c_result = canonical(values.copy())
    g_result = generated(values.copy())
    print(
        f"input={values!r} formal_expected={expected} "
        f"canonical={c_result} generated={g_result}"
    )
    if c_result is not expected or g_result is not expected:
        raise SystemExit(1)
print(f"ground_python_mismatch_count=0 count={len(cases)}")
PY
status=$?
echo "exit=$status"
(( status == 0 )) || overall=1

exit "$overall"
