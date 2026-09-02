#!/usr/bin/env bash
set -u
set -o pipefail

scratch=/tmp/audit-work/5-intersperse
evidence=/audit-output/evidence
overall=0

run_logged() {
  local name="$1"
  shift
  local log="$evidence/$name"
  printf 'COMMAND'
  printf ' %q' "$@"
  printf '\nLOG %s\n' "$log"
  "$@" >"$log" 2>&1
  local status=$?
  printf 'EXIT %d\n' "$status"
  if [[ -s "$log" ]]; then
    printf 'OUTPUT_BEGIN\n'
    tail -n 120 "$log"
    printf 'OUTPUT_END\n'
  fi
  return "$status"
}

printf 'Fresh toolchain versions\n'
kompile --version
kprove --version
krun --version

printf 'Concrete harness body identity check\n'
python3 - "$scratch/solution.py" "$evidence/03_k_concrete_tests.py" <<'PY'
import ast
import sys

def function_dump(path):
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    return ast.dump(function, include_attributes=False)

left = function_dump(sys.argv[1])
right = function_dump(sys.argv[2])
print(f"function_ast_identity={left == right}")
raise SystemExit(0 if left == right else 1)
PY
ast_status=$?
printf 'function_ast_check_exit=%d\n' "$ast_status"
if [[ "$ast_status" -ne 0 ]]; then
  overall=1
fi

run_logged 03_translate_concrete.log \
  python3 "$scratch/py2mpy.py" "$evidence/03_k_concrete_tests.py"
translate_status=$?
if [[ "$translate_status" -eq 0 ]]; then
  cp "$evidence/03_translate_concrete.log" "$scratch/auditor-concrete-tests.mpy"
else
  overall=1
fi

run_logged 03_kompile_llvm.log \
  kompile "$scratch/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$scratch/runtime-kompiled"
llvm_build_status=$?
if [[ "$llvm_build_status" -ne 0 ]]; then
  overall=1
fi

if [[ "$llvm_build_status" -eq 0 && "$translate_status" -eq 0 ]]; then
  run_logged 03_krun_concrete.log \
    krun "$scratch/auditor-concrete-tests.mpy" \
    --definition "$scratch/runtime-kompiled"
  concrete_status=$?
  if [[ "$concrete_status" -ne 0 ]]; then
    overall=1
  fi
else
  printf 'SKIP concrete run because build or translation failed\n'
  overall=1
fi

run_logged 03_kompile_haskell.log \
  kompile "$scratch/verification.k" \
  --backend haskell \
  --main-module INTERSPERSE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$scratch/verification-kompiled"
haskell_build_status=$?
if [[ "$haskell_build_status" -ne 0 ]]; then
  overall=1
fi

if [[ "$haskell_build_status" -eq 0 ]]; then
  run_logged 03_kprove_all.log \
    kprove "$scratch/spec.k" \
    --definition "$scratch/verification-kompiled" \
    --spec-module INTERSPERSE-SPEC
  prove_status=$?
  if [[ "$prove_status" -ne 0 ]] || ! grep -Fxq '#Top' "$evidence/03_kprove_all.log"; then
    overall=1
  fi
  printf 'kprove_exit=%d exact_top=%s\n' \
    "$prove_status" \
    "$(if grep -Fxq '#Top' "$evidence/03_kprove_all.log"; then printf YES; else printf NO; fi)"
else
  printf 'SKIP positive proof because Haskell build failed\n'
  overall=1
fi

printf 'RECONSTRUCTION_SCRIPT_STATUS=%d\n' "$overall"
exit "$overall"
