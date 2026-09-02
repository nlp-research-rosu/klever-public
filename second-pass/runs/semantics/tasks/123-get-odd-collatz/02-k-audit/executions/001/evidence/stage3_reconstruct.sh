#!/usr/bin/env bash
set -u
set -o pipefail

src=/tmp/audit-work/123-get-odd-collatz/proof-src
evidence=/audit-output/evidence

run_log() {
  local log_file=$1
  shift
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local command_rc=$?
    printf '[exit %d]\n' "$command_rc"
    return "$command_rc"
  } 2>&1 | tee "$log_file"
  local pipeline_rc=${PIPESTATUS[0]}
  printf '[recorded exit %d in %s]\n' "$pipeline_rc" "$log_file"
  return 0
}

printf 'Stage 3 clean reconstruction\n'
run_log "$evidence/tool_versions.log" kompile --version
run_log "$evidence/kprove_help_claims.log" kprove --help

printf '\nRegenerate the concrete harness with the trusted translator\n'
printf '$ cd %q && python3 %q %q > %q\n' \
  "$src" /tmp/audit-work/123-get-odd-collatz/trusted/py2mpy.py \
  concrete_tests.py concrete_tests.regenerated.mpy
(
  cd "$src" || exit 125
  python3 /tmp/audit-work/123-get-odd-collatz/trusted/py2mpy.py \
    concrete_tests.py > concrete_tests.regenerated.mpy
)
regen_rc=$?
printf '[exit %d]\n' "$regen_rc"

printf '\nBuild a new LLVM concrete definition from trusted supplied semantics\n'
(
  cd "$src" || exit 125
  run_log "$evidence/stage3_kompile_llvm.log" \
    kompile reference-semantics/semantics.k \
      --backend llvm \
      --main-module MPY-KRUN \
      --syntax-module MPY-SYNTAX \
      --output-definition runtime-kompiled-audit
)

printf '\nExecute the independently regenerated concrete assertion harness\n'
(
  cd "$src" || exit 125
  run_log "$evidence/stage3_krun_concrete.log" \
    krun concrete_tests.regenerated.mpy \
      --definition runtime-kompiled-audit \
      --output none
)

printf '\nBuild a new Haskell proof definition from source\n'
(
  cd "$src" || exit 125
  run_log "$evidence/stage3_kompile_haskell.log" \
    kompile verification.k \
      --backend haskell \
      --main-module VERIFICATION \
      --syntax-module VERIFICATION \
      --output-definition verification-kompiled-audit
)

printf '\nRun every positive target claim independently\n'
for label in odd-step even-step exit-step case-1 case-5 case-6 case-7; do
  (
    cd "$src" || exit 125
    run_log "$evidence/stage3_kprove_${label}.log" \
      kprove spec.k \
        --definition verification-kompiled-audit \
        --spec-module SPEC \
        --claims "SPEC.$label" \
        --depth 2000 \
        --smt-timeout 5000
  )
done

printf '\nRun the aggregate positive target spec\n'
(
  cd "$src" || exit 125
  run_log "$evidence/stage3_kprove_all.log" \
    kprove spec.k \
      --definition verification-kompiled-audit \
      --spec-module SPEC \
      --depth 2000 \
      --smt-timeout 5000
)
