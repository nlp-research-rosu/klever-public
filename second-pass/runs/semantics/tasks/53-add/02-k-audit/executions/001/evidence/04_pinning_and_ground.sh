#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/04_pinning_and_ground.log
WORK=/tmp/audit-work/53-add
export PATH="/home/agent/.nix-profile/bin:$PATH"
exec >"$LOG" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

run python3 /audit-output/evidence/program_pin.py || exit $?
run cp /audit-output/evidence/ground-tests.mpy "$WORK/ground-tests.mpy" || exit $?
run cp /audit-output/evidence/spec-ground.k "$WORK/spec-ground.k" || exit $?

printf '\n$ cd %q\n' "$WORK"
cd "$WORK" || exit 1
printf '[exit 0]\n'

run krun ground-tests.mpy --definition runtime-kompiled || exit $?
run kprove spec-ground.k \
  --definition verification-kompiled \
  --spec-module ADD-SPEC-GROUND || exit $?

printf '\n$ python3 - <<PY\n'
python3 - <<'PY'
import importlib.util
from pathlib import Path

work = Path("/tmp/audit-work/53-add")

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

canonical = load(work / "trusted" / "canonical.py", "ground_canonical")
candidate = load(work / "solution.py", "ground_candidate")
for x, y in [(2, 3), (0, 0), (-10, 3), (2**63 - 1, 1), (10**100, -(10**100))]:
    print((x, y), canonical.add(x, y), candidate.add(x, y), x + y)
PY
rc=$?
printf '[exit %d]\n' "$rc"
exit "$rc"
