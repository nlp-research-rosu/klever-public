#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/106-f
source_dir="$work/source"
build_dir="$work/build"
evidence=/audit-output/evidence
export PATH="$HOME/.nix-profile/bin:$PATH"

if [ -e "$build_dir/semantic-kompiled" ] || [ -e "$build_dir/verification-kompiled" ]; then
  echo 'FRESHNESS_FAILURE: requested output definition already exists'
  exit 98
fi

echo 'COMMAND: kompile --version && kprove --version'
kompile --version
version_one=$?
kprove --version
version_two=$?
echo "KOMPILE_VERSION_EXIT_STATUS: $version_one"
echo "KPROVE_VERSION_EXIT_STATUS: $version_two"

echo 'COMMAND: fresh LLVM build from copied semantic.k source'
(
  cd "$source_dir" &&
  kompile semantic.k \
    --main-module SEMANTIC \
    --syntax-module MPY-SYNTAX \
    --backend llvm \
    --output-definition "$build_dir/semantic-kompiled"
) 2>&1 | tee "$evidence/02_kompile_semantic.log"
semantic_build_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $semantic_build_status" | tee -a "$evidence/02_kompile_semantic.log"
if [ "$semantic_build_status" -ne 0 ]; then
  exit "$semantic_build_status"
fi

echo 'COMMAND: concrete comparison script over fresh LLVM semantics'
python3 "$evidence/02_concrete_compare.py" 2>&1 | tee "$evidence/02_concrete_compare.log"
concrete_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $concrete_status" | tee -a "$evidence/02_concrete_compare.log"
if [ "$concrete_status" -ne 0 ]; then
  exit "$concrete_status"
fi

echo 'COMMAND: fresh Haskell proof-definition build from copied verification.k source'
(
  cd "$source_dir" &&
  kompile verification.k \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --backend haskell \
    --output-definition "$build_dir/verification-kompiled"
) 2>&1 | tee "$evidence/02_kompile_verification.log"
proof_build_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $proof_build_status" | tee -a "$evidence/02_kompile_verification.log"
if [ "$proof_build_status" -ne 0 ]; then
  exit "$proof_build_status"
fi

echo 'COMMAND: expand submitted solution.mpy and solution macro to KORE, then compare'
(
  cd "$source_dir" &&
  kast solution.mpy \
    --definition "$build_dir/verification-kompiled" \
    --module VERIFICATION \
    --sort Program \
    --expand-macros \
    --output kore > "$build_dir/submitted-solution.kore"
)
submitted_kast_status=$?
(
  cd "$source_dir" &&
  kast \
    --expression solution \
    --definition "$build_dir/verification-kompiled" \
    --module VERIFICATION \
    --sort Program \
    --expand-macros \
    --output kore > "$build_dir/macro-solution.kore"
)
macro_kast_status=$?
cmp "$build_dir/submitted-solution.kore" "$build_dir/macro-solution.kore"
ast_cmp_status=$?
sha256sum "$build_dir/submitted-solution.kore" "$build_dir/macro-solution.kore"
echo "SUBMITTED_KAST_EXIT_STATUS: $submitted_kast_status"
echo "MACRO_KAST_EXIT_STATUS: $macro_kast_status"
echo "AST_CMP_EXIT_STATUS: $ast_cmp_status"
if [ "$submitted_kast_status" -ne 0 ] || [ "$macro_kast_status" -ne 0 ] || [ "$ast_cmp_status" -ne 0 ]; then
  exit 1
fi

echo 'COMMAND: independently prove SPEC.loop-invariant only'
(
  cd "$source_dir" &&
  kprove spec.k \
    --definition "$build_dir/verification-kompiled" \
    --spec-module SPEC \
    --claims SPEC.loop-invariant \
    --output pretty
) 2>&1 | tee "$evidence/02_kprove_loop_invariant.log"
loop_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $loop_status" | tee -a "$evidence/02_kprove_loop_invariant.log"

echo 'COMMAND: independently prove SPEC.main-correct only'
(
  cd "$source_dir" &&
  kprove spec.k \
    --definition "$build_dir/verification-kompiled" \
    --spec-module SPEC \
    --claims SPEC.main-correct \
    --output pretty
) 2>&1 | tee "$evidence/02_kprove_main_correct.log"
main_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $main_status" | tee -a "$evidence/02_kprove_main_correct.log"

echo 'COMMAND: prove all positive claims together'
(
  cd "$source_dir" &&
  kprove spec.k \
    --definition "$build_dir/verification-kompiled" \
    --spec-module SPEC \
    --output pretty
) 2>&1 | tee "$evidence/02_kprove_all.log"
all_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $all_status" | tee -a "$evidence/02_kprove_all.log"

echo 'COMMAND: verify each successful proof log contains exact #Top line'
top_status=0
for proof_log in \
  "$evidence/02_kprove_loop_invariant.log" \
  "$evidence/02_kprove_main_correct.log" \
  "$evidence/02_kprove_all.log"; do
  if ! rg -x '#Top' "$proof_log"; then
    top_status=1
  fi
done
echo "EXIT_STATUS: $top_status"

if [ "$loop_status" -eq 0 ] && [ "$main_status" -eq 0 ] && [ "$all_status" -eq 0 ] && [ "$top_status" -eq 0 ]; then
  exit 0
fi
exit 1
