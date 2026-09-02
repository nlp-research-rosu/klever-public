#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/124-valid-date
EVIDENCE=/audit-output/evidence

run_bounded() {
  local label=$1
  shift
  local raw="$WORK/${label}.raw.log"
  local log="$EVIDENCE/${label}.log"

  {
    printf 'WORKDIR: %s\n' "$WORK"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } >"$log"

  (
    cd "$WORK"
    "$@"
  ) >"$raw" 2>&1
  local status=$?

  {
    printf '%s\n' 'OUTPUT_HEAD:'
    sed -n '1,120p' "$raw"
    printf '%s\n' 'OUTPUT_TAIL:'
    tail -n 160 "$raw"
    printf 'EXIT_STATUS: %s\n' "$status"
  } >>"$log"
  printf '%s exit=%s\n' "$label" "$status"
  tail -n 20 "$log"
  return "$status"
}

export PATH="/root/.nix-profile/bin:$PATH"

find "$WORK" -maxdepth 1 -type d -name '*-kompiled' -print

run_bounded 03a_kompile_llvm \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
LLVM_BUILD_STATUS=$?

(
  cd "$WORK"
  python3 trusted_py2mpy.py 03_concrete_tests.py > 03_concrete_tests.mpy
)
TRANSLATE_STATUS=$?
printf '03b_translate_concrete exit=%s\n' "$TRANSLATE_STATUS"

run_bounded 03c_krun_concrete \
  krun 03_concrete_tests.mpy \
  --definition audit-runtime-kompiled
KRUN_STATUS=$?

run_bounded 03d_kompile_haskell \
  kompile verification.k \
  --backend haskell \
  --main-module VALID-DATE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
HASKELL_BUILD_STATUS=$?

run_bounded 03e_kprove_length_not_ten \
  kprove spec-length-not-ten.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-LENGTH-NOT-TEN
CLAIM1_STATUS=$?

run_bounded 03f_kprove_length_ten \
  kprove spec-length-ten.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-LENGTH-TEN
CLAIM2_STATUS=$?

run_bounded 03g_kprove_original_combined \
  kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module VALID-DATE-SPEC
COMBINED_STATUS=$?

SUMMARY="$EVIDENCE/03_reconstruction_summary.log"
{
  printf 'llvm_build_status=%s\n' "$LLVM_BUILD_STATUS"
  printf 'concrete_translation_status=%s\n' "$TRANSLATE_STATUS"
  printf 'krun_status=%s\n' "$KRUN_STATUS"
  printf 'haskell_build_status=%s\n' "$HASKELL_BUILD_STATUS"
  printf 'claim_length_not_ten_status=%s\n' "$CLAIM1_STATUS"
  printf 'claim_length_ten_status=%s\n' "$CLAIM2_STATUS"
  printf 'combined_original_status=%s\n' "$COMBINED_STATUS"
  printf 'claim_length_not_ten_top_count='
  rg -c '^#Top$' "$WORK/03e_kprove_length_not_ten.raw.log" || true
  printf 'claim_length_ten_top_count='
  rg -c '^#Top$' "$WORK/03f_kprove_length_ten.raw.log" || true
  printf 'combined_original_top_count='
  rg -c '^#Top$' "$WORK/03g_kprove_original_combined.raw.log" || true
  printf 'concrete_final_k_count='
  rg -c '^[[:space:]]+\\.K$' "$WORK/03c_krun_concrete.raw.log" || true
} >"$SUMMARY"
sed -n '1,160p' "$SUMMARY"

if [ "$LLVM_BUILD_STATUS" -ne 0 ] ||
   [ "$TRANSLATE_STATUS" -ne 0 ] ||
   [ "$KRUN_STATUS" -ne 0 ] ||
   [ "$HASKELL_BUILD_STATUS" -ne 0 ] ||
   [ "$CLAIM1_STATUS" -ne 0 ] ||
   [ "$CLAIM2_STATUS" -ne 0 ] ||
   [ "$COMBINED_STATUS" -ne 0 ]; then
  exit 1
fi
