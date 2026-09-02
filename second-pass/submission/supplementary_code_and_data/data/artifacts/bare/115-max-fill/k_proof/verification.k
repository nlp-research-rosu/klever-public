requires "semantic.k"
requires "solution-program.k"

module VERIFICATION
  imports SOLUTION-PROGRAM

  // Mathematical specification: count the water in a row, then sum one
  // ceiling-division per well.  These equations do not mention the Python AST
  // or its helper function names.
  syntax Int ::= "water" "(" Ints ")" [function]
  rule water(.Ints) => 0
  rule water(I, REST) => I +Int water(REST)

  syntax Int ::= "requiredBuckets" "(" Rows "," Int ")" [function]
  rule requiredBuckets(.Rows, C) => 0
  rule requiredBuckets(rowVal(ROW), ROWS, C)
    => ((water(ROW) +Int C -Int 1) /Int C)
       +Int requiredBuckets(ROWS, C)
    requires C >Int 0

  syntax Map ::= "solutionFunctions" [function]
  syntax Map ::= functionsOf(Module) [function]
  rule functionsOf(Module(SS)) => collectFunctions(SS)
  rule solutionFunctions => functionsOf(solutionProgram)
endmodule
