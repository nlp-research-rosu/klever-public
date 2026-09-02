#!/usr/bin/env bash
set -u

status=0
scratch=/tmp/audit-work/reconstruction
runtime_definition="$scratch/fresh-runtime-kompiled"
proof_definition="$scratch/fresh-verification-kompiled"

printf 'COMMAND: bash /audit-output/evidence/03_reconstruction.sh\n'
printf 'INFO source root=%s\n' "$scratch"
printf 'INFO candidate-provided kompiled directories were not copied\n'
printf 'RUN: kompile --version\n'
kompile --version
printf 'RUN: kprove --version\n'
kprove --version

if [[ -e "$runtime_definition" || -e "$proof_definition" ]]; then
  printf 'FAIL fresh output path already exists\n'
  exit 2
fi

printf 'STAGE: mechanically verify reviewer concrete-test function equals submitted function\n'
python3 - <<'PY'
import ast
from pathlib import Path

def first_function(path):
    tree = ast.parse(Path(path).read_text())
    return next(node for node in tree.body if isinstance(node, ast.FunctionDef))

solution = first_function("/tmp/audit-work/reconstruction/solution.py")
driver = first_function("/audit-output/evidence/k_concrete_tests.py")
same = ast.dump(solution, include_attributes=False) == ast.dump(driver, include_attributes=False)
print(f"AST function identity={same}")
raise SystemExit(0 if same else 1)
PY
ast_status=$?
printf 'EXIT AST function identity: %d\n' "$ast_status"
if [[ "$ast_status" -ne 0 ]]; then
  status=1
fi

printf 'RUN: python3 trusted py2mpy.py reviewer concrete test\n'
python3 "$scratch/py2mpy.py" /audit-output/evidence/k_concrete_tests.py > "$scratch/k_concrete_tests.mpy"
translate_status=$?
printf 'EXIT concrete translation: %d\n' "$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: clean LLVM definition build from trusted supplied semantics\n'
printf 'RUN: kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition fresh-runtime-kompiled\n'
(
  cd "$scratch" || exit 98
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition fresh-runtime-kompiled
)
llvm_status=$?
printf 'EXIT LLVM kompile: %d\n' "$llvm_status"
if [[ "$llvm_status" -ne 0 ]]; then
  status=1
fi

printf 'RUN: krun k_concrete_tests.mpy --definition fresh-runtime-kompiled\n'
(
  cd "$scratch" || exit 98
  krun k_concrete_tests.mpy --definition fresh-runtime-kompiled
)
krun_status=$?
printf 'EXIT concrete krun: %d\n' "$krun_status"
if [[ "$krun_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: clean Haskell proof definition build from candidate proof sources and trusted supplied semantics\n'
printf 'RUN: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled\n'
(
  cd "$scratch" || exit 98
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition fresh-verification-kompiled
)
haskell_status=$?
printf 'EXIT Haskell kompile: %d\n' "$haskell_status"
if [[ "$haskell_status" -ne 0 ]]; then
  status=1
fi

printf 'STAGE: independently run each positive target claim\n'
printf 'RUN: kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.scan-loop\n'
(
  cd "$scratch" || exit 98
  kprove spec.k \
    --definition fresh-verification-kompiled \
    --spec-module SPEC \
    --claims SPEC.scan-loop
)
scan_status=$?
printf 'EXIT scan-loop kprove: %d\n' "$scan_status"
if [[ "$scan_status" -ne 0 ]]; then
  status=1
fi

printf 'INFO entry-point-correct depends on scan-loop; selecting only the entry claim removes its circularity, so the required target run is the unfiltered SPEC invocation containing both claims\n'
printf 'RUN: kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC\n'
(
  cd "$scratch" || exit 98
  kprove spec.k \
    --definition fresh-verification-kompiled \
    --spec-module SPEC
)
combined_status=$?
printf 'EXIT combined kprove: %d\n' "$combined_status"
if [[ "$combined_status" -ne 0 ]]; then
  status=1
fi

printf 'FINAL EXIT: %d\n' "$status"
exit "$status"
