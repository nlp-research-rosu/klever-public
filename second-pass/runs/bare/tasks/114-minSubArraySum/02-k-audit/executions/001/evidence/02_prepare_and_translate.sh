#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/114-minSubArraySum-audit

run() {
  local cmd="$1"
  printf '$ %s\n' "$cmd"
  bash -o pipefail -c "$cmd"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run "mkdir -p '$SCRATCH'"
run "cp /candidate/solution.py '$SCRATCH/solution.py'"
run "cp /candidate/solution.mpy '$SCRATCH/submitted-solution.mpy'"
run "cp /candidate/semantic.k '$SCRATCH/semantic.k'"
run "cp /candidate/verification.k '$SCRATCH/verification.k'"
run "cp /candidate/spec.k '$SCRATCH/spec.k'"
run "cp /reference/canonical.py '$SCRATCH/canonical.py'"
run "cp /reference/py2mpy.py '$SCRATCH/trusted-py2mpy.py'"
run "python3 '$SCRATCH/trusted-py2mpy.py' '$SCRATCH/solution.py' > '$SCRATCH/solution.mpy'"
run "cmp -s '$SCRATCH/solution.mpy' '$SCRATCH/submitted-solution.mpy'"
run "sha256sum '$SCRATCH/solution.py' '$SCRATCH/solution.mpy' '$SCRATCH/submitted-solution.mpy'"
run "python3 -m py_compile '$SCRATCH/solution.py' '$SCRATCH/canonical.py'"
run "find '$SCRATCH' -maxdepth 1 -printf '%y %f -> %l\n' | LC_ALL=C sort"
