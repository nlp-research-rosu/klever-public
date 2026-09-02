requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  syntax Int ::= fibMath(Int) [function]

  rule fibMath(N) => N
    requires 0 <=Int N andBool N <=Int 1
  rule fibMath(N) => fibMath(N -Int 1) +Int fibMath(N -Int 2)
    requires N >Int 1
endmodule
