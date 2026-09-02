#!/usr/bin/env bash
set -u

work=/tmp/audit-work/46-fib4-audit/candidate-src
evidence=/audit-output/evidence

run_logged() {
  local tag=$1
  shift
  local log="$evidence/$tag.log"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1 | tee "$log"
  local rc=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$rc" | tee -a "$log"
  return 0
}

run_logged stage4_ast_identity python3 -c '
import ast
from pathlib import Path
a = ast.parse(Path("/candidate/solution.py").read_text()).body[0]
b = ast.parse(Path("/audit-output/evidence/stage4_program_cases.py").read_text()).body[0]
print("function_ast_equal:", ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False))
raise SystemExit(0 if ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False) else 1)
'

run_logged stage4_translate bash -c \
  'python3 /reference/py2mpy.py /audit-output/evidence/stage4_program_cases.py > /tmp/audit-work/46-fib4-audit/candidate-src/stage4-program-cases.mpy'

run_logged stage4_krun timeout 120s \
  krun "$work/stage4-program-cases.mpy" \
  --definition "$work/runtime-kompiled" \
  --output pretty
