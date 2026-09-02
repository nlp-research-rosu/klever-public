#!/usr/bin/env bash
set -u

root=/tmp/audit-work/reconstruction
source_dir="$root/candidate-src"
mutant_py="$root/pinning-mutant.py"
pinning_case="$root/pinning-case"
mutant_mpy="$pinning_case/solution.mpy"
haskell_def="$root/fresh-haskell-kompiled"
llvm_def="$root/fresh-llvm-kompiled"
failed=0

run_and_report() {
  echo 'AUDITOR COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  echo "EXIT STATUS: $status"
  return "$status"
}

echo 'MUTATION: change the real Python body tail from depth == 0 to depth == 1.'
echo 'AUDITOR COMMAND: create isolated source case with unchanged K files and mutated solution.py'
mkdir -p "$pinning_case"
cp "$source_dir/semantic.k" "$source_dir/verification.k" \
  "$source_dir/audit-spec.k" "$pinning_case/"
cp "$mutant_py" "$pinning_case/solution.py"
copy_status=$?
echo "EXIT STATUS: $copy_status"
if (( copy_status != 0 )); then
  failed=1
fi

echo "AUDITOR COMMAND: python3 $root/reference/py2mpy.py $pinning_case/solution.py > $mutant_mpy"
python3 "$root/reference/py2mpy.py" "$pinning_case/solution.py" > "$mutant_mpy"
translator_status=$?
echo "EXIT STATUS: $translator_status"
if (( translator_status != 0 )); then
  failed=1
fi

run_and_report cmp -s "$mutant_mpy" "$source_dir/solution.mpy"
cmp_status=$?
echo "EXPECTED DIFFERENCE: cmp status should be 1; observed=$cmp_status"
if (( cmp_status != 1 )); then
  failed=1
fi

echo 'The mutant is demonstrably wrong on satisfying intended-domain input "<".'
run_and_report python3 -c \
  'import importlib.util; p="/tmp/audit-work/reconstruction/pinning-mutant.py"; s=importlib.util.spec_from_file_location("m",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.correct_bracketing("<")); raise SystemExit(m.correct_bracketing("<") is not True)'
python_status=$?
if (( python_status != 0 )); then
  failed=1
fi

run_and_report krun "$mutant_mpy" --definition "$llvm_def" '-cINPUT="<"'
krun_status=$?
if (( krun_status != 0 )); then
  failed=1
fi

echo 'Now rerun the purported universal proof without changing semantic.k.'
echo 'The current directory now contains the mutant as solution.mpy.'
echo 'The claim still proves correctProgram(), showing that kprove never reads solution.mpy.'
cd "$pinning_case" || exit 2
run_and_report kprove audit-spec.k \
  --definition "$haskell_def" \
  --spec-module AUDIT-SPEC \
  --claims AUDIT-SPEC.loop-zero,AUDIT-SPEC.loop-positive,AUDIT-SPEC.universal-correctness
proof_status=$?
if (( proof_status != 0 )); then
  failed=1
fi

echo "AGGREGATE UNEXPECTED-OUTCOME FLAG: $failed"
exit "$failed"
