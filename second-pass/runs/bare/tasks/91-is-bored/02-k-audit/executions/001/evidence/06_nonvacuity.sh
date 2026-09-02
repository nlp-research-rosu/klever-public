#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
status=0

printf '%s\n' 'COMMAND: cmp /tmp/audit-work/reconstruction/spec-vacuity.k /audit-output/evidence/spec-vacuity.k'
cmp "$work/spec-vacuity.k" /audit-output/evidence/spec-vacuity.k
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: python3 -c canonical/submitted witness for "Hello world"'
python3 -c '
import importlib.util
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored
canonical = load("canonical_vacuity", "/reference/canonical.py")
submitted = load("submitted_vacuity", "/tmp/audit-work/reconstruction/solution.py")
text = "Hello world"
print(f"input={text!r} canonical={canonical(text)} submitted={submitted(text)} mutated_expected=1")
assert canonical(text) == submitted(text) == 0
'
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: timeout 120s kprove spec-vacuity.k --definition verification-fresh-kompiled --spec-module SPEC-VACUITY --dry-run'
(
  cd "$work" &&
    timeout 120s kprove spec-vacuity.k \
      --definition verification-fresh-kompiled \
      --spec-module SPEC-VACUITY \
      --dry-run
)
code=$?
printf 'DRY_RUN_EXIT: %s\n' "$code"
(( code == 0 )) || status=1

printf '%s\n' 'COMMAND: timeout 120s kprove spec-vacuity.k --definition verification-fresh-kompiled --spec-module SPEC-VACUITY'
output=$(
  cd "$work" &&
    timeout 120s kprove spec-vacuity.k \
      --definition verification-fresh-kompiled \
      --spec-module SPEC-VACUITY 2>&1
)
proof_code=$?
printf '%s\n' "$output"
printf 'PROOF_EXIT: %s\n' "$proof_code"
if (( proof_code == 0 )); then
  status=1
fi

printf '%s\n' 'COMMAND: check residual for expected stuck implication/result obligation'
printf '%s\n' "$output" |
  rg 'WarnStuckClaimState|implication check.*failed|<result>|Lbl'-n
grep_code=$?
printf 'RESIDUAL_CHECK_EXIT: %s\n' "$grep_code"
(( grep_code == 0 )) || status=1

exit "$status"
