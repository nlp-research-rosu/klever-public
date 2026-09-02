requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports INT

  syntax Int ::= sumToN(Int) [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY

  rule sumToN(N) => N *Int (N +Int 1) /Int 2
    requires N >=Int 0
  rule sumToN(N) => 0
    requires N <Int 0
endmodule
