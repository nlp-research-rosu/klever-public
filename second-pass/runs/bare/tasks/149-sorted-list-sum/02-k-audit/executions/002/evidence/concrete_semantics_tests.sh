#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/reconstruction
definition="$scratch/concrete-kompiled"

run_case() {
  local name=$1
  local expression=$2
  local python_expected=$3
  local k_expected=$4
  local run_file="$scratch/reviewer-${name}.run"
  local out_file="$scratch/reviewer-${name}.out"

  (
    cd "$scratch"
    python3 make_run.py "$expression"
  ) > "$run_file"

  printf 'CASE %s\n' "$name"
  printf 'INPUT_CONSTRUCTOR %s\n' "$expression"
  printf 'EXPECTED_PYTHON %s\n' "$python_expected"
  krun "$run_file" --definition "$definition" --output pretty > "$out_file"
  sed -n '1,20p' "$out_file"
  grep -Fq "$k_expected" "$out_file"
  printf 'K_RESULT_MATCH true\n'
}

run_case \
  empty-list \
  'Call(Name("sorted_list_sum"), ListExpr())' \
  '[]' \
  'VList ( .Words )'

run_case \
  empty-string \
  'Call(Name("sorted_list_sum"), ListExpr(Str("")))' \
  '[""]' \
  'VList ( "" , .Words )'

run_case \
  all-odd \
  'Call(Name("sorted_list_sum"), ListExpr(Str("a"), Str("abc"), Str("12345")))' \
  '[]' \
  'VList ( .Words )'

run_case \
  prompt-boundary \
  'Call(Name("sorted_list_sum"), ListExpr(Str("ab"), Str("a"), Str("aaa"), Str("cd")))' \
  '["ab", "cd"]' \
  'VList ( "ab" , "cd" , .Words )'

run_case \
  duplicates-and-key-ties \
  'Call(Name("sorted_list_sum"), ListExpr(Str("zy"), Str("ab"), Str("x"), Str("aa"), Str("abcd"), Str("ba"), Str("ab")))' \
  '["aa", "ab", "ab", "ba", "zy", "abcd"]' \
  'VList ( "aa" , "ab" , "ab" , "ba" , "zy" , "abcd" , .Words )'

run_case \
  length-boundaries \
  'Call(Name("sorted_list_sum"), ListExpr(Str(""), Str("a"), Str("aa"), Str("bbb"), Str("cccc")))' \
  '["", "aa", "cccc"]' \
  'VList ( "" , "aa" , "cccc" , .Words )'

run_case \
  symbolic-two-witness \
  'Call(Name("sorted_list_sum"), ListExpr(Str("aa"), Str("ab")))' \
  '["aa", "ab"]' \
  'VList ( "aa" , "ab" , .Words )'

run_case \
  symbolic-two-reverse-witness \
  'Call(Name("sorted_list_sum"), ListExpr(Str("ba"), Str("ab")))' \
  '["ab", "ba"]' \
  'VList ( "ab" , "ba" , .Words )'

run_case \
  symbolic-three-witness \
  'Call(Name("sorted_list_sum"), ListExpr(Str("zzzz"), Str("aa"), Str("bbb")))' \
  '["aa", "zzzz"]' \
  'VList ( "aa" , "zzzz" , .Words )'

printf 'CONCRETE_SEMANTICS_OK cases=9\n'
