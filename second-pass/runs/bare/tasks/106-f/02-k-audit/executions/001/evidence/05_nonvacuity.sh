#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/106-f
source_dir="$work/source"
definition="$work/build/verification-kompiled"
evidence=/audit-output/evidence
export PATH="$HOME/.nix-profile/bin:$PATH"

echo 'COMMAND: preserve and diff fresh mutation'
cp -p "$source_dir/spec-vacuity.k" "$evidence/spec-vacuity.k"
diff -u "$source_dir/spec.k" "$source_dir/spec-vacuity.k" || true
sha256sum "$source_dir/spec-vacuity.k" "$evidence/spec-vacuity.k"

echo 'SATISFYING WITNESS: N=0; actual result [] versus deliberately required [0]'
python3 - <<'PY'
import importlib.util
from pathlib import Path

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f

root = Path("/tmp/audit-work/106-f")
canonical = load(root / "reference/canonical.py", "mutation_canonical")
generated = load(root / "source/solution.py", "mutation_generated")
print(f"canonical(0)={canonical(0)!r}")
print(f"generated(0)={generated(0)!r}")
print("mutated_required=[0]")
PY
witness_status=$?
echo "EXIT_STATUS: $witness_status"

echo 'COMMAND: kprove mutated spec --dry-run (must parse/build)'
(
  cd "$source_dir" &&
  kprove spec-vacuity.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY \
    --dry-run
) 2>&1 | tee "$evidence/05_vacuity_dry_run.log"
dry_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $dry_status" | tee -a "$evidence/05_vacuity_dry_run.log"

echo 'COMMAND: kprove fresh false mutation (expected semantic proof failure)'
(
  cd "$source_dir" &&
  timeout 180 kprove spec-vacuity.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY \
    --output pretty
) 2>&1 | tee "$evidence/05_vacuity_kprove.log"
proof_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $proof_status" | tee -a "$evidence/05_vacuity_kprove.log"

echo 'COMMAND: verify expected stuck-claim diagnostic'
rg -n 'WarnStuckClaimState|implication check|ListItem|expected' "$evidence/05_vacuity_kprove.log"
residual_status=$?
echo "EXIT_STATUS: $residual_status"

if [ "$witness_status" -eq 0 ] && \
   [ "$dry_status" -eq 0 ] && \
   [ "$proof_status" -ne 0 ] && \
   [ "$proof_status" -ne 124 ] && \
   [ "$residual_status" -eq 0 ]; then
  echo 'NON_VACUITY_RESULT: PASS (false reachable obligation rejected)'
  exit 0
fi
echo 'NON_VACUITY_RESULT: FAIL'
exit 1
