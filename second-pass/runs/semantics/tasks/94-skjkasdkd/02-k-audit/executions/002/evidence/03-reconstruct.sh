#!/usr/bin/env bash
set -u

evidence=/audit-output/evidence
overall=0

run_logged() {
  local name="$1"
  shift
  local log="$evidence/$name.log"
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    rc=$?
    echo "EXIT_STATUS=$rc"
  } > "$log" 2>&1
  echo "$name exit=$rc"
  if (( rc != 0 )); then
    overall=1
  fi
}

echo "COMMAND: compare concrete harness function AST to solution.py"
python3 -c '
import ast
from pathlib import Path
def fn(path):
    tree = ast.parse(Path(path).read_text(), filename=path)
    return next(n for n in tree.body if isinstance(n, ast.FunctionDef))
assert ast.dump(fn("solution.py"), include_attributes=False) == ast.dump(
    fn("concrete-audit.py"), include_attributes=False
)
print("function ASTs identical")
' > "$evidence/03-concrete-ast.log" 2>&1
ast_rc=$?
echo "EXIT_STATUS=$ast_rc" >> "$evidence/03-concrete-ast.log"
echo "concrete-ast exit=$ast_rc"
(( ast_rc == 0 )) || overall=1

{
  echo "COMMAND: python3 py2mpy.py concrete-audit.py > concrete-audit.mpy"
  python3 py2mpy.py concrete-audit.py > concrete-audit.mpy
  rc=$?
  echo "EXIT_STATUS=$rc"
} > "$evidence/03-concrete-translate.log" 2>&1
echo "concrete-translate exit=$rc"
(( rc == 0 )) || overall=1

run_logged 03-kompile-llvm \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled

run_logged 03-krun-concrete \
  krun concrete-audit.mpy \
  --definition reviewer-runtime-kompiled

run_logged 03-kompile-haskell \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition reviewer-verification-kompiled \
  -I .

run_logged 03-kprove-prime-loop \
  kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.prime-loop \
  --output pretty

run_logged 03-kprove-digit-loop \
  kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.digit-loop \
  --output pretty

run_logged 03-kprove-scan-loop \
  kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --trusted SPEC.prime-loop,SPEC.digit-loop \
  --output pretty

run_logged 03-kprove-entry-prefix \
  kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --trusted SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --output pretty

run_logged 03-kprove-main-correct \
  kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.main-correct,SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --trusted SPEC.entry-prefix,SPEC.scan-loop,SPEC.prime-loop,SPEC.digit-loop \
  --output pretty

for label in prime-loop digit-loop scan-loop entry-prefix main-correct; do
  log="$evidence/03-kprove-$label.log"
  if [[ -f "$log" ]] \
    && grep -Fxq '#Top' "$log" \
    && grep -Fxq 'EXIT_STATUS=0' "$log"; then
    echo "$label SUCCESS: exit 0 and #Top"
  else
    echo "$label FAILURE: missing exit 0 or #Top"
    overall=1
  fi
done

echo "FINAL_STATUS=$overall"
exit "$overall"
