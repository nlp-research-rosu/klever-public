#!/usr/bin/env bash
set -u

root=/tmp/audit-work/reconstruction
source_dir="$root/candidate-src"
definition="$root/fresh-haskell-kompiled"
unexpected=0

echo 'AUDITOR COMMAND: cmp scratch mutation preserved evidence mutation'
cmp -s "$source_dir/audit-spec-vacuity.k" \
  /audit-output/evidence/06_spec_vacuity.k
cmp_status=$?
echo "EXIT STATUS: $cmp_status"
if (( cmp_status != 0 )); then
  unexpected=1
fi

echo 'SATISFYING WITNESS: intended-domain input "<>" makes both Python implementations return true.'
echo 'AUDITOR COMMAND: execute trusted canonical and candidate Python on "<>"'
python3 -c \
  'import importlib.util
paths=["/tmp/audit-work/reconstruction/reference/canonical.py","/tmp/audit-work/reconstruction/candidate-src/solution.py"]
values=[]
for index,path in enumerate(paths):
    spec=importlib.util.spec_from_file_location(f"m{index}",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    values.append(module.correct_bracketing("<>"))
print(values)
raise SystemExit(values != [True, True])'
python_status=$?
echo "EXIT STATUS: $python_status"
if (( python_status != 0 )); then
  unexpected=1
fi

cd "$source_dir" || exit 2

echo 'AUDITOR COMMAND: parse/build the mutated claim with kprove --dry-run'
kprove audit-spec-vacuity.k \
  --definition "$definition" \
  --spec-module AUDIT-SPEC-VACUITY \
  --claims AUDIT-SPEC-VACUITY.false-pair \
  --dry-run
dry_status=$?
echo "EXIT STATUS: $dry_status"
if (( dry_status != 0 )); then
  unexpected=1
fi

echo 'AUDITOR COMMAND: prove the deliberately false mutated claim'
proof_output=$(
  kprove audit-spec-vacuity.k \
    --definition "$definition" \
    --spec-module AUDIT-SPEC-VACUITY \
    --claims AUDIT-SPEC-VACUITY.false-pair 2>&1
)
proof_status=$?
printf '%s\n' "$proof_output"
echo "EXIT STATUS: $proof_status (nonzero expected)"
if (( proof_status == 0 )); then
  unexpected=1
fi
if grep -Fq 'WarnStuckClaimState' <<< "$proof_output"; then
  echo 'EXPECTED RESIDUAL CHECK: WarnStuckClaimState present'
else
  echo 'EXPECTED RESIDUAL CHECK: WarnStuckClaimState absent'
  unexpected=1
fi
if grep -Fq 'result ( BVal ( true ) )' <<< "$proof_output"; then
  echo 'EXPECTED UNMET OBLIGATION CHECK: residual contains actual true result'
else
  echo 'EXPECTED UNMET OBLIGATION CHECK: actual true result not found'
  unexpected=1
fi

echo "AGGREGATE UNEXPECTED-OUTCOME FLAG: $unexpected"
exit "$unexpected"
