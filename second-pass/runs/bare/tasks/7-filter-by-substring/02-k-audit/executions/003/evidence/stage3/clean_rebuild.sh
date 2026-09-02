#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/source
build_dir=/tmp/audit-work/build
concrete_definition="$build_dir/concrete-kompiled"
proof_definition="$build_dir/proof-kompiled"
status=0

print_command() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
}

run() {
  print_command "$@"
  "$@"
  rc=$?
  printf 'EXIT: %d\n' "$rc"
  if [[ "$rc" -ne 0 ]]; then
    status=1
  fi
}

run_top() {
  print_command "$@"
  output=$("$@" 2>&1)
  rc=$?
  printf '%s\n' "$output"
  printf 'EXIT: %d\n' "$rc"
  top_count=$(printf '%s\n' "$output" | awk '$0 == "#Top" { count += 1 } END { print count + 0 }')
  printf 'EXACT_TOP_LINES: %d\n' "$top_count"
  if [[ "$rc" -ne 0 || "$top_count" -lt 1 ]]; then
    status=1
  fi
}

run_krun_expect() {
  expected=$1
  shift
  print_command "$@"
  output=$("$@" 2>&1)
  rc=$?
  printf '%s\n' "$output"
  printf 'EXIT: %d\n' "$rc"
  if [[ "$rc" -ne 0 || "$output" != "$expected" ]]; then
    printf 'EXPECTED EXACT OUTPUT:\n%s\n' "$expected"
    printf 'MATCH: false\n'
    status=1
  else
    printf 'MATCH: true\n'
  fi
}

run kompile --version
run kprove --version
run krun --version

run rm -rf -- "$concrete_definition"
run rm -rf -- "$proof_definition"

run kompile "$source_dir/semantic.k" \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition "$concrete_definition"

run kompile "$source_dir/verification.k" \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition "$proof_definition"

printf '%s\n' '$ python3 - (independent Python results for concrete K cases)'
PYTHONPATH="$source_dir" python3 - <<'PY'
from canonical import filter_by_substring as canonical
from solution import filter_by_substring as candidate

cases = [
    ([], "a"),
    (["abc", "bacd", "cde", "array"], "a"),
    (["x", "x", ""], ""),
    ([""], ""),
    (["", "a", "ab"], "zz"),
    (["é", "café", "e\u0301"], "é"),
]
for strings, substring in cases:
    print(
        f"strings={strings!r} substring={substring!r} "
        f"canonical={canonical(strings, substring)!r} "
        f"candidate={candidate(strings, substring)!r}"
    )
PY
rc=$?
printf 'EXIT: %d\n' "$rc"
if [[ "$rc" -ne 0 ]]; then
  status=1
fi

run_krun_expect $'<k>\n  Nil ~> .K\n</k>' \
  krun "$source_dir/solution.mpy" \
  --definition "$concrete_definition" \
  -cFUNCTION='"filter_by_substring"' \
  -cINPUT='Nil' \
  -cSUBSTRING='"a"'

run_krun_expect $'<k>\n  Cons ( "abc" , Cons ( "bacd" , Cons ( "array" , Nil ) ) ) ~> .K\n</k>' \
  krun "$source_dir/solution.mpy" \
  --definition "$concrete_definition" \
  -cFUNCTION='"filter_by_substring"' \
  -cINPUT='Cons("abc",Cons("bacd",Cons("cde",Cons("array",Nil))))' \
  -cSUBSTRING='"a"'

run_krun_expect $'<k>\n  Cons ( "x" , Cons ( "x" , Cons ( "" , Nil ) ) ) ~> .K\n</k>' \
  krun "$source_dir/solution.mpy" \
  --definition "$concrete_definition" \
  -cFUNCTION='"filter_by_substring"' \
  -cINPUT='Cons("x",Cons("x",Cons("",Nil)))' \
  -cSUBSTRING='""'

run_krun_expect $'<k>\n  Cons ( "" , Nil ) ~> .K\n</k>' \
  krun "$source_dir/solution.mpy" \
  --definition "$concrete_definition" \
  -cFUNCTION='"filter_by_substring"' \
  -cINPUT='Cons("",Nil)' \
  -cSUBSTRING='""'

run_krun_expect $'<k>\n  Nil ~> .K\n</k>' \
  krun "$source_dir/solution.mpy" \
  --definition "$concrete_definition" \
  -cFUNCTION='"filter_by_substring"' \
  -cINPUT='Cons("",Cons("a",Cons("ab",Nil)))' \
  -cSUBSTRING='"zz"'

run_krun_expect $'<k>\n  Cons ( "\\xe9" , Cons ( "caf\\xe9" , Nil ) ) ~> .K\n</k>' \
  krun "$source_dir/solution.mpy" \
  --definition "$concrete_definition" \
  -cFUNCTION='"filter_by_substring"' \
  -cINPUT='Cons("é",Cons("café",Cons("é",Nil)))' \
  -cSUBSTRING='"é"'

claims=(
  UNIVERSAL-PROGRAM-REDUCTION
  UNIVERSAL-BASE
  UNIVERSAL-STEP-KEEP
  UNIVERSAL-STEP-DROP
  EMPTY-EXAMPLE
  PROMPT-EXAMPLE
)

for claim in "${claims[@]}"; do
  run_top kprove "$source_dir/spec.k" \
    --definition "$proof_definition" \
    --spec-module SPEC \
    --claims "$claim"
done

exit "$status"
