requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports INT-SYNTAX

  // The prompt's Fib4 recurrence, totalized to 0 below the stated N >= 0 domain.
  syntax Int ::= fib4Spec(Int) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  rule fib4Spec(N) => 0
    requires N <=Int 0
  rule fib4Spec(1) => 0
  rule fib4Spec(2) => 2
  rule fib4Spec(3) => 0
  rule fib4Spec(N)
    => fib4Spec(N -Int 1) +Int fib4Spec(N -Int 2)
       +Int fib4Spec(N -Int 3) +Int fib4Spec(N -Int 4)
    requires N >=Int 4
endmodule
