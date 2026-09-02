#!/usr/bin/env bash
set -u

scratch="/tmp/audit-work/37-sort-even"
evidence="/audit-output/evidence"
summary="$evidence/04-body-sensitivity-summary.log"
mut_ver_e="$evidence/04-verification-step3.k"
mut_spec_e="$evidence/04-spec-step3.k"
mut_ver="$scratch/verification-step3.k"
mut_spec="$scratch/spec-step3.k"
mut_def="$scratch/verification-step3-kompiled"

printf '%s\n' \
  "COMMAND: sed -e '3s/module VERIFICATION/module VERIFICATION-STEP3/' -e '22s/Int(2)/Int(3)/' verification.k > 04-verification-step3.k" \
  "COMMAND: sed -e '1s/verification.k/verification-step3.k/' -e '3s/module SPEC/module SPEC-STEP3/' -e '4s/imports VERIFICATION/imports VERIFICATION-STEP3/' spec.k > 04-spec-step3.k" \
  > "$summary"

sed \
  -e '3s/module VERIFICATION/module VERIFICATION-STEP3/' \
  -e '22s/Int(2)/Int(3)/' \
  "$scratch/verification.k" > "$mut_ver_e"
ver_make_status=$?
sed \
  -e '1s/verification.k/verification-step3.k/' \
  -e '3s/module SPEC/module SPEC-STEP3/' \
  -e '4s/imports VERIFICATION/imports VERIFICATION-STEP3/' \
  "$scratch/spec.k" > "$mut_spec_e"
spec_make_status=$?
cp -a "$mut_ver_e" "$mut_ver"
ver_copy_status=$?
cp -a "$mut_spec_e" "$mut_spec"
spec_copy_status=$?
diff -u "$scratch/verification.k" "$mut_ver_e" > "$evidence/04-body-sensitivity.diff"
diff_status=$?
printf 'VERIFICATION_MUTATION_CREATE_EXIT_STATUS: %s\n' "$ver_make_status" >> "$summary"
printf 'SPEC_MUTATION_CREATE_EXIT_STATUS: %s\n' "$spec_make_status" >> "$summary"
printf 'VERIFICATION_COPY_EXIT_STATUS: %s\n' "$ver_copy_status" >> "$summary"
printf 'SPEC_COPY_EXIT_STATUS: %s\n' "$spec_copy_status" >> "$summary"
printf 'EXPECTED_NONZERO_DIFF_EXIT_STATUS: %s\n' "$diff_status" >> "$summary"

build_log="$evidence/04-body-sensitivity-build.log"
printf '%s\n' \
  'COMMAND: kompile verification-step3.k --backend haskell --main-module VERIFICATION-STEP3 --syntax-module MPY-SYNTAX -I . --output-definition verification-step3-kompiled' \
  > "$build_log"
(
  cd "$scratch" &&
  kompile verification-step3.k \
    --backend haskell \
    --main-module VERIFICATION-STEP3 \
    --syntax-module MPY-SYNTAX \
    -I . \
    --output-definition "$mut_def"
) >> "$build_log" 2>&1
build_status=$?
printf 'EXIT_STATUS: %s\n' "$build_status" >> "$build_log"
printf 'BUILD_EXIT_STATUS: %s\n' "$build_status" >> "$summary"

loop_log="$evidence/04-body-sensitivity-loop.log"
printf '%s\n' \
  'COMMAND: kprove spec-step3.k --definition verification-step3-kompiled --spec-module SPEC-STEP3 --claims SPEC-STEP3.loop-correct --output pretty' \
  > "$loop_log"
if [ "$build_status" -eq 0 ]; then
  (
    cd "$scratch" &&
    kprove spec-step3.k \
      --definition "$mut_def" \
      --spec-module SPEC-STEP3 \
      --claims SPEC-STEP3.loop-correct \
      --output pretty
  ) >> "$loop_log" 2>&1
  loop_status=$?
else
  loop_status=1
fi
printf 'EXIT_STATUS: %s\n' "$loop_status" >> "$loop_log"
printf 'UNCHANGED_LOOP_EXIT_STATUS: %s\n' "$loop_status" >> "$summary"

entry_log="$evidence/04-body-sensitivity-entry.log"
printf '%s\n' \
  'COMMAND: kprove spec-step3.k --definition verification-step3-kompiled --spec-module SPEC-STEP3 --claims SPEC-STEP3.loop-correct,SPEC-STEP3.sort-even-correct --trusted SPEC-STEP3.loop-correct --output pretty' \
  > "$entry_log"
if [ "$build_status" -eq 0 ] && [ "$loop_status" -eq 0 ]; then
  (
    cd "$scratch" &&
    kprove spec-step3.k \
      --definition "$mut_def" \
      --spec-module SPEC-STEP3 \
      --claims SPEC-STEP3.loop-correct,SPEC-STEP3.sort-even-correct \
      --trusted SPEC-STEP3.loop-correct \
      --output pretty
  ) >> "$entry_log" 2>&1
  entry_status=$?
else
  entry_status=0
fi
printf 'EXIT_STATUS: %s\n' "$entry_status" >> "$entry_log"
printf 'EXPECTED_NONZERO_ENTRY_EXIT_STATUS: %s\n' "$entry_status" >> "$summary"

if [ "$ver_make_status" -ne 0 ] || [ "$spec_make_status" -ne 0 ] || \
   [ "$ver_copy_status" -ne 0 ] || [ "$spec_copy_status" -ne 0 ] || \
   [ "$diff_status" -eq 0 ] || [ "$build_status" -ne 0 ] || \
   [ "$loop_status" -ne 0 ] || [ "$entry_status" -eq 0 ]; then
  printf '%s\n' 'OVERALL_EXIT_STATUS: 1' >> "$summary"
  exit 1
fi
printf '%s\n' 'OVERALL_EXIT_STATUS: 0' >> "$summary"
exit 0
