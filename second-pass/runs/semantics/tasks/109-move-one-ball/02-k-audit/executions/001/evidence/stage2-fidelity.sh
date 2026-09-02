#!/usr/bin/env bash
set +e

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n\n' "$status"
}

run_shell() {
  printf '$ %s\n' "$1"
  bash -o pipefail -c "$1"
  status=$?
  printf '[exit %d]\n\n' "$status"
}

run_shell "python3 /reference/py2mpy.py /tmp/audit-work/109-move-one-ball/candidate/solution.py > /audit-output/evidence/solution.regenerated.mpy"
run cmp -s /audit-output/evidence/solution.regenerated.mpy /tmp/audit-work/109-move-one-ball/candidate/solution.mpy
run sha256sum /audit-output/evidence/solution.regenerated.mpy /tmp/audit-work/109-move-one-ball/candidate/solution.mpy
run python3 /audit-output/evidence/differential.py
