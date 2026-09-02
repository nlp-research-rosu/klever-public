#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run krun solution.mpy \
  --definition semantic-audit-kompiled \
  '-cENTRY="minSubArraySum"' \
  '-cARGS=pyList(cons(2, cons(3, cons(4, cons(1, cons(2, cons(4, nil)))))))'

run krun solution.mpy \
  --definition semantic-audit-kompiled \
  '-cENTRY="minSubArraySum"' \
  '-cARGS=pyList(cons(-1, cons(-2, cons(-3, nil))))'

run krun solution.mpy \
  --definition semantic-audit-kompiled \
  '-cENTRY="minSubArraySum"' \
  '-cARGS=pyList(cons(7, nil))'

run krun solution.mpy \
  --definition semantic-audit-kompiled \
  '-cENTRY="minSubArraySum"' \
  '-cARGS=pyList(cons(0, cons(0, nil)))'

run krun solution.mpy \
  --definition semantic-audit-kompiled \
  '-cENTRY="minSubArraySum"' \
  '-cARGS=pyList(cons(5, cons(-7, nil)))'

run krun solution.mpy \
  --definition semantic-audit-kompiled \
  '-cENTRY="minSubArraySum"' \
  '-cARGS=pyList(cons(4, cons(-6, cons(2, cons(-5, cons(7, nil))))))'

run krun solution.mpy \
  --definition semantic-audit-kompiled \
  '-cENTRY="minSubArraySum"' \
  '-cARGS=pyList(cons(1000000000000000000000000000000, cons(-10000000000000000000000000000000, cons(1000000000000000000000000000000, nil))))'
