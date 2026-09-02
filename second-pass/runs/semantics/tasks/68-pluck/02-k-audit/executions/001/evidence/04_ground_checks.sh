#!/usr/bin/env bash
set +e
cd /tmp/audit-work/68-pluck || exit 90

run_bounded() {
  local label=$1
  shift
  local raw="/tmp/audit-work/68-pluck/${label}.raw.log"
  echo "\$ $*"
  "$@" >"$raw" 2>&1
  local rc=$?
  local lines
  lines=$(wc -l <"$raw")
  echo "exit=$rc lines=$lines"
  if (( lines <= 120 )); then
    sed -n '1,120p' "$raw"
  else
    sed -n '1,60p' "$raw"
    echo "... [bounded log: middle omitted] ..."
    tail -60 "$raw"
  fi
  return "$rc"
}

echo '$ python3 /reference/py2mpy.py ground_tests.py > ground_tests.mpy'
python3 /reference/py2mpy.py ground_tests.py > ground_tests.mpy
translate_rc=$?
echo "exit=$translate_rc"

if (( translate_rc == 0 )); then
  run_bounded 04a_krun_ground_tests \
    krun ground_tests.mpy --definition runtime-audit-kompiled
  krun_rc=$?
else
  krun_rc=99
fi

run_bounded 04b_kprove_ground_summary \
  kprove ground-summary-spec.k \
    --definition proof-audit-kompiled \
    --spec-module GROUND-SUMMARY-SPEC \
    --output pretty
summary_rc=$?

run_bounded 04c_python_ground \
  python3 /audit-output/evidence/04_ground_python.py
python_rc=$?

echo "SUMMARY translate=$translate_rc krun=$krun_rc summary=$summary_rc python=$python_rc"
if (( translate_rc != 0 || krun_rc != 0 || summary_rc != 0 || python_rc != 0 )); then
  exit 1
fi
