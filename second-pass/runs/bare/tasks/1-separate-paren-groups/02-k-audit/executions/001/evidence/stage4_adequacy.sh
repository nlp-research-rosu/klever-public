#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return 0
}

run cp \
  /audit-output/evidence/ground-witnesses.k \
  /tmp/audit-work/candidate/ground-witnesses.k
run python3 /audit-output/evidence/pinning_check.py

cd /tmp/audit-work/candidate || exit 99

run kprove ground-witnesses.k \
  --definition verification-haskell-kompiled \
  --spec-module GROUND-WITNESSES \
  --claims GROUND-WITNESSES.loop-ground \
  --output pretty
run kprove ground-witnesses.k \
  --definition verification-haskell-kompiled \
  --spec-module GROUND-WITNESSES \
  --claims GROUND-WITNESSES.program-ground \
  --output pretty
run python3 -c \
  'import importlib.util; p="/tmp/audit-work/trusted/canonical.py"; s=importlib.util.spec_from_file_location("c",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.separate_paren_groups("()"))'
run python3 -c \
  'import importlib.util; p="/tmp/audit-work/candidate/solution.py"; s=importlib.util.spec_from_file_location("s",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.separate_paren_groups("()"))'
