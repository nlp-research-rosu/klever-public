requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX

  // Mathematical result of testing the candidate divisors D, D+1, ..., N-1.
  // The function is intentionally defined only on the proof domain D >= 2.
  syntax Bool ::= trialPrime(Int, Int, Bool) [function]
  syntax Bool ::= primeNat(Int) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX
  imports BOOL
  imports INT

  rule trialPrime(N, D, P) => P
    requires D >=Int N andBool D >=Int 2

  rule trialPrime(N, D, P) => trialPrime(N, D +Int 1, false)
    requires D <Int N andBool D >=Int 2
     andBool pyMod(N, D) ==Int 0

  rule trialPrime(N, D, P) => trialPrime(N, D +Int 1, P)
    requires D <Int N andBool D >=Int 2
     andBool pyMod(N, D) =/=Int 0

  rule primeNat(N) => trialPrime(N, 2, N >=Int 2)
endmodule
