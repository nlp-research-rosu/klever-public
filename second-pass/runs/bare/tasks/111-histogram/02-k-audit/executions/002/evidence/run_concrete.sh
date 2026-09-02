#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/fresh

run_case() {
  local audit_input="$1"
  local audit_k_string="\"${audit_input}\""
  printf 'INPUT=%q\n' "$audit_input"
  python3 - "$audit_input" <<'PY'
import importlib.util
import sys
from pathlib import Path

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram

value = sys.argv[1]
canonical = load("canonical", Path("/reference/canonical.py"))
generated = load("generated", Path("/tmp/audit-work/fresh/solution.py"))
print(f"PY_CANONICAL={canonical(value)!r}")
print(f"PY_GENERATED={generated(value)!r}")
PY
  printf 'COMMAND=krun solution.mpy --definition semantic-llvm-kompiled -cTEST=%q --output pretty\n' "$audit_k_string"
  krun solution.mpy \
    --definition semantic-llvm-kompiled \
    -cTEST="$audit_k_string" \
    --output pretty
}

run_case ""
run_case "a"
run_case "a a"
run_case "a a b"
run_case "a b b"
run_case "a a b b c"
run_case "a b c a b"
run_case " a"
run_case "a  b"
