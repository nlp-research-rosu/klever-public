requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical result for positive integer endpoints.  These four cases
  // are exhaustive over Int and do not replace any MPY execution step.
  syntax Int ::= chooseNumSpec(Int, Int) [function, total]

  rule chooseNumSpec(X, Y) => -1
    requires X >Int Y

  rule chooseNumSpec(X, Y) => Y
    requires X <=Int Y
     andBool pyMod(Y, 2) ==Int 0

  rule chooseNumSpec(X, Y) => Y -Int 1
    requires X <=Int Y
     andBool pyMod(Y, 2) =/=Int 0
     andBool Y -Int 1 >=Int X

  rule chooseNumSpec(X, Y) => -1
    requires X <=Int Y
     andBool pyMod(Y, 2) =/=Int 0
     andBool Y -Int 1 <Int X
endmodule
