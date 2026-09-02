#!/usr/bin/env bash
set -u
export PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate
definition="$work/semantic-concrete-kompiled"
program="$work/solution.mpy"

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return 0
}

run krun "$program" --definition "$definition" \
  -cARGS='args(pyList(.StrVals),pyList(.StrVals))'
run krun "$program" --definition "$definition" \
  -cARGS='args(pyList(pyStr("hi") :: pyStr("admin") :: .StrVals),pyList(pyStr("hI") :: pyStr("Hi") :: .StrVals))'
run krun "$program" --definition "$definition" \
  -cARGS='args(pyList(pyStr("") :: .StrVals),pyList(pyStr("a") :: .StrVals))'
run krun "$program" --definition "$definition" \
  -cARGS='args(pyList(pyStr("ab") :: .StrVals),pyList(pyStr("c") :: .StrVals))'
run krun "$program" --definition "$definition" \
  -cARGS='args(pyList(pyStr("") :: pyStr("ab") :: .StrVals),pyList(pyStr("a") :: pyStr("b") :: .StrVals))'
run krun "$program" --definition "$definition" \
  -cARGS='args(pyList(pyStr("é") :: .StrVals),pyList(pyStr("é") :: .StrVals))'
run krun "$program" --definition "$definition" \
  -cARGS='args(pyList(pyStr("😀") :: .StrVals),pyList(pyStr("ab") :: .StrVals))'

printf '%s\n' 'COMMAND: python3 (independent CPython comparison for the seven K cases)'
python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.total_match

canonical = load("canonical", "/reference/canonical.py")
candidate = load("candidate", "/tmp/audit-work/candidate/solution.py")
cases = [
    ([], []),
    (["hi", "admin"], ["hI", "Hi"]),
    ([""], ["a"]),
    (["ab"], ["c"]),
    (["", "ab"], ["a", "b"]),
    (["é"], ["e\u0301"]),
    (["😀"], ["ab"]),
]
for index, (first, second) in enumerate(cases):
    print(
        index,
        "totals=", (sum(map(len, first)), sum(map(len, second))),
        "canonical=", repr(canonical(first, second)),
        "candidate=", repr(candidate(first, second)),
    )
PY
printf 'EXIT: %d\n' "$?"
