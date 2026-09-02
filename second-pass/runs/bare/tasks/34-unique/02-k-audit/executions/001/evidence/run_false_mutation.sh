#!/usr/bin/env bash
set -uo pipefail
PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cd /tmp/audit-work/34-unique
nl -ba spec-vacuity.k

kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
dry_run_status=$?

kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY
proof_status=$?

python3 -c \
  'import sys; sys.path.insert(0, "reference"); import canonical; sys.path[0] = "candidate-source"; import solution; print("WITNESS=[]"); print("CANONICAL_RESULT=", canonical.unique([])); print("GENERATED_RESULT=", solution.unique([])); assert canonical.unique([]) == solution.unique([]) == []'
witness_status=$?

set +x
printf 'MUTATION_DRY_RUN_EXIT_STATUS=%s\n' "$dry_run_status"
printf 'MUTATION_PROOF_EXIT_STATUS=%s\n' "$proof_status"
printf 'WITNESS_EXECUTION_EXIT_STATUS=%s\n' "$witness_status"
if (( dry_run_status || proof_status == 0 || witness_status )); then
  exit 1
fi
exit 0
