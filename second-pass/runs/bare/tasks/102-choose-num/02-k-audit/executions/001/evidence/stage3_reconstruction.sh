#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/stage3-reconstruction.log
exec > >(tee "$LOG") 2>&1

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run_capture() {
  local output=$1
  shift
  printf '$'
  printf ' %q' "$@"
  printf ' | tee %q\n' "$output"
  "$@" | tee "$output"
  local status=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work || exit 1
status=0
printf 'STAGE 3 CLEAN PROOF RECONSTRUCTION\n'
run test ! -e concrete-kompiled || status=1
run test ! -e proof-kompiled || status=1

run kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled || status=1

run kompile semantic.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled || status=1

printf 'fresh definition identity\n'
run cat concrete-kompiled/mainModule.txt || status=1
run cat proof-kompiled/mainModule.txt || status=1
run sha256sum concrete-kompiled/definition.kore proof-kompiled/definition.kore || status=1

cases=(
  '12 15 14 normal_prompt_example'
  '13 12 -1 empty_interval'
  '13 13 -1 odd_singleton'
  '12 12 12 even_singleton'
  '1 2 2 smallest_even_endpoint'
  '2 3 2 odd_upper_with_room'
  '1 1 -1 smallest_positive_boundary'
  '999999999999 1000000000000 1000000000000 large_boundary'
)

for row in "${cases[@]}"; do
  read -r x y expected label <<<"$row"
  input="run-${label}.mpy"
  output="run-${label}.out"
  run python3 /audit-output/evidence/make_run_term.py "$x" "$y" "$input" || status=1
  run python3 /audit-output/evidence/concrete_oracle.py "$x" "$y" "$expected" || status=1
  run_capture "$output" krun "$input" --definition concrete-kompiled || status=1
  run grep -F "VInt ( $expected )" "$output" || status=1
done

printf 'original aggregate target proof\n'
run kprove spec.k --definition proof-kompiled --spec-module SPEC || status=1

printf 'eight independent positive target-proof claims\n'
for claim_number in 01 02 03 04 05 06 07 08; do
  run kprove "spec-${claim_number}.k" \
    --definition proof-kompiled \
    --spec-module "SPEC${claim_number}" || status=1
done

printf 'stage3_status=%d\n' "$status"
exit "$status"
