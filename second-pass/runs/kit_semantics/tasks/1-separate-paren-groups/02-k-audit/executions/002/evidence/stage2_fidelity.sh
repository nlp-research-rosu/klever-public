#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/reconstruction

run_cmd() {
  local command_text="$1"
  printf '\n$ %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run_cmd "mkdir -p '$SCRATCH'"
run_cmd "cp -a /reference/reference-semantics '$SCRATCH/reference-semantics'"
run_cmd "cp /reference/prompt.py '$SCRATCH/prompt.py'"
run_cmd "cp /reference/canonical.py '$SCRATCH/canonical.py'"
run_cmd "cp /reference/py2mpy.py '$SCRATCH/py2mpy.py'"
run_cmd "cp /candidate/solution.py /candidate/solution.mpy /candidate/verification.k /candidate/spec.k /candidate/spec-vacuity.k /candidate/spec-body-mutation.k '$SCRATCH/'"
run_cmd "find -P '$SCRATCH' -maxdepth 3 -printf '%y %P %s\\n' | sort"
run_cmd "cd '$SCRATCH' && python3 py2mpy.py solution.py > regenerated-solution.mpy"
run_cmd "cmp -s '$SCRATCH/regenerated-solution.mpy' /candidate/solution.mpy && echo 'translation byte identity: yes'"
run_cmd "sha256sum '$SCRATCH/regenerated-solution.mpy' /candidate/solution.mpy"
run_cmd "python3 /audit-output/evidence/differential_audit.py"
