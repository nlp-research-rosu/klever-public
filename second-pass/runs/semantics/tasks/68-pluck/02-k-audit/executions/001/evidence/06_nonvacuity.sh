#!/usr/bin/env bash
set +e
cd /tmp/audit-work/68-pluck || exit 90

show_bounded() {
  local raw=$1
  local lines
  lines=$(wc -l <"$raw")
  echo "lines=$lines"
  if (( lines <= 180 )); then
    sed -n '1,180p' "$raw"
  else
    sed -n '1,90p' "$raw"
    echo "... [bounded log: middle omitted] ..."
    tail -90 "$raw"
  fi
}

echo '$ diff -u spec.k spec-vacuity.k'
diff -u spec.k spec-vacuity.k
diff_rc=$?
echo "exit=$diff_rc (1 means the intended difference was present)"

dry_raw=/tmp/audit-work/68-pluck/06a_vacuity_dry_run.raw.log
echo '$ kprove spec-vacuity.k --definition proof-audit-kompiled --spec-module PLUCK-SPEC --claims PLUCK-SPEC.pluck-correct,PLUCK-SPEC.pluck-loop --trusted PLUCK-SPEC.pluck-loop --dry-run'
kprove spec-vacuity.k \
  --definition proof-audit-kompiled \
  --spec-module PLUCK-SPEC \
  --claims PLUCK-SPEC.pluck-correct,PLUCK-SPEC.pluck-loop \
  --trusted PLUCK-SPEC.pluck-loop \
  --dry-run >"$dry_raw" 2>&1
dry_rc=$?
echo "exit=$dry_rc"
show_bounded "$dry_raw"

proof_raw=/tmp/audit-work/68-pluck/06b_vacuity_proof.raw.log
echo '$ timeout 300s kprove spec-vacuity.k --definition proof-audit-kompiled --spec-module PLUCK-SPEC --claims PLUCK-SPEC.pluck-correct,PLUCK-SPEC.pluck-loop --trusted PLUCK-SPEC.pluck-loop --output pretty'
timeout 300s kprove spec-vacuity.k \
  --definition proof-audit-kompiled \
  --spec-module PLUCK-SPEC \
  --claims PLUCK-SPEC.pluck-correct,PLUCK-SPEC.pluck-loop \
  --trusted PLUCK-SPEC.pluck-loop \
  --output pretty >"$proof_raw" 2>&1
proof_rc=$?
echo "exit=$proof_rc"
show_bounded "$proof_raw"

echo '$ python3 -c "import importlib.util; s=importlib.util.spec_from_file_location('\''s'\'','\''solution.py'\''); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.pluck([4,2,3]))"'
python3 -c "import importlib.util; s=importlib.util.spec_from_file_location('s','solution.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.pluck([4,2,3]))"
witness_rc=$?
echo "exit=$witness_rc"

if (( diff_rc != 1 || dry_rc != 0 || proof_rc == 0 || proof_rc == 124 || witness_rc != 0 )); then
  exit 1
fi
if ! rg -q 'WarnStuckClaimState|cannot be rewritten further|implication check' "$proof_raw"; then
  echo 'expected unmet-obligation diagnostic not found'
  exit 1
fi
exit 0
