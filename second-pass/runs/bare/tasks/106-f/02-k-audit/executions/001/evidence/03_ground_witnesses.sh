#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/106-f
source_dir="$work/source"
definition="$work/build/audit-ground-kompiled-2"
evidence=/audit-output/evidence
export PATH="$HOME/.nix-profile/bin:$PATH"

if [ -e "$definition" ]; then
  echo 'FRESHNESS_FAILURE: audit-ground-kompiled already exists'
  exit 98
fi

echo 'COMMAND: fresh LLVM build of reviewer ground-expression harness'
(
  cd "$source_dir" &&
  kompile audit-ground.k \
    --main-module AUDIT-GROUND \
    --syntax-module AUDIT-GROUND \
    --backend llvm \
    --output-definition "$definition"
) 2>&1 | tee "$evidence/03_kompile_ground_harness.log"
build_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $build_status" | tee -a "$evidence/03_kompile_ground_harness.log"
if [ "$build_status" -ne 0 ]; then
  exit "$build_status"
fi

overall=0
for program in expected-ground-0.mpy expected-ground-5.mpy loop-completion-ground.mpy; do
  echo "COMMAND: krun $program --definition $definition"
  (
    cd "$source_dir" &&
    krun "$program" -cINPUT=0 --definition "$definition" --output pretty
  ) 2>&1 | tee "$evidence/03_${program%.mpy}.log"
  run_status=${PIPESTATUS[0]}
  echo "EXIT_STATUS: $run_status" | tee -a "$evidence/03_${program%.mpy}.log"
  if [ "$run_status" -ne 0 ]; then
    overall=1
  fi
done

echo 'PYTHON COMPARISON COMMAND: canonical.py and solution.py at n=0 and n=5'
python3 - <<'PY'
import importlib.util
from pathlib import Path

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f

root = Path("/tmp/audit-work/106-f")
canonical = load(root / "reference/canonical.py", "ground_canonical")
generated = load(root / "source/solution.py", "ground_generated")
for n in (0, 5):
    print(f"n={n} canonical={canonical(n)!r} generated={generated(n)!r}")
PY
python_status=$?
echo "EXIT_STATUS: $python_status"

if [ "$overall" -eq 0 ] && [ "$python_status" -eq 0 ]; then
  exit 0
fi
exit 1
