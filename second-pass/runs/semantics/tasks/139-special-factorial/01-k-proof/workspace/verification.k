requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical factorial, defined on all integers so that the functions
  // used in claims are total.  The proof only uses non-negative arguments.
  syntax Int ::= factorial(Int) [function, total]
  rule factorial(N:Int) => 1
       requires N <=Int 0
  rule factorial(N:Int) => factorial(N -Int 1) *Int N
       requires N >Int 0

  // Product 1! * 2! * ... * n!, equal to the prompt's reversed product.
  syntax Int ::= specialFactorial(Int) [function, total]
  rule specialFactorial(N:Int) => 1
       requires N <=Int 0
  rule specialFactorial(N:Int)
    => specialFactorial(N -Int 1) *Int factorial(N)
       requires N >Int 0
endmodule
