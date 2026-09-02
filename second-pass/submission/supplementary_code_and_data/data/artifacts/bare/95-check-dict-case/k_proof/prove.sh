#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

cd "$(dirname "$0")"

program_tmp="program.k.tmp"
run_tmp="krun-result.tmp"
proof_tmp="kprove-result.tmp"
trap 'rm -f "$program_tmp" "$run_tmp" "$proof_tmp"' EXIT

# Recreate the pure AST transliteration required by the task.
python3 py2mpy.py solution.py > solution.mpy

# Tie the proof constant mechanically to that exact transliteration.  K source
# files contain modules, so the bare term is wrapped in a generated module.
{
  printf '%s\n\n' 'requires "semantic.k"'
  printf '%s\n' 'module SOLUTION-PROGRAM'
  printf '%s\n\n' '  imports MPY-SYNTAX'
  printf '%s\n' '  syntax PyStmt ::= "solutionProgram" [function]'
  printf '%s' '  rule solutionProgram => '
  sed '2,$s/^/  /' solution.mpy
  printf '%s\n' 'endmodule'
} > "$program_tmp"
mv "$program_tmp" program.k

# A small CPython smoke test also guards the submitted implementation itself.
python3 - <<'PY'
from solution import check_dict_case

cases = [
    ({}, False),
    ({"a": "apple", "b": "banana"}, True),
    ({"a": "apple", "A": "banana", "B": "banana"}, False),
    ({"a": "apple", 8: "banana"}, False),
    ({"Name": "John", "Age": "36", "City": "Houston"}, False),
    ({"STATE": "NC", "ZIP": "12345"}, True),
    ({"abc-123": 0, "z9": 0}, True),
    ({"123": 0}, False),
]
for dictionary, expected in cases:
    assert check_dict_case(dictionary) is expected
print("CPython smoke tests: passed")
PY

# Compile the semantics used by both concrete execution and symbolic proof.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell

check_krun() {
  local input="$1"
  local expected="$2"
  krun solution.mpy \
    --definition verification-kompiled \
    "-cINPUT=$input" \
    --pattern '<result> R:Value </result>' \
    --output pretty > "$run_tmp"
  grep -Fq "BoolVal ( $expected )" "$run_tmp"
}

# Exercise every example class through the actual solution.mpy parser.
check_krun 'DictVal()' false
check_krun 'DictVal(StrVal("a") StrVal("b"))' true
check_krun 'DictVal(StrVal("a") StrVal("A") StrVal("B"))' false
check_krun 'DictVal(StrVal("a") IntVal(8))' false
check_krun 'DictVal(StrVal("Name") StrVal("Age") StrVal("City"))' false
check_krun 'DictVal(StrVal("STATE") StrVal("ZIP"))' true
echo "krun examples: passed"

# This is the required positive target-proof command.  pipefail preserves the
# kprove exit status, while the final grep insists on its exact success term.
kprove spec.k --definition verification-kompiled | tee "$proof_tmp"
grep -qx '#Top' "$proof_tmp"
