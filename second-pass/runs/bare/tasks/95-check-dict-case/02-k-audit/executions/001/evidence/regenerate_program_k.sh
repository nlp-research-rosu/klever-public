#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/candidate-src
output="$scratch/program.regenerated.k"

{
  printf '%s\n\n' 'requires "semantic.k"'
  printf '%s\n' 'module SOLUTION-PROGRAM'
  printf '%s\n\n' '  imports MPY-SYNTAX'
  printf '%s\n' '  syntax PyStmt ::= "solutionProgram" [function]'
  printf '%s' '  rule solutionProgram => '
  sed '2,$s/^/  /' "$scratch/solution.regenerated.mpy"
  printf '%s\n' 'endmodule'
} > "$output"
generation_status=$?
echo "wrapper generation status: $generation_status"

cmp "$scratch/program.k" "$output"
cmp_status=$?
echo "submitted-vs-regenerated program.k cmp status: $cmp_status"

sha256sum "$scratch/program.k" "$output"

(( generation_status == 0 && cmp_status == 0 ))
