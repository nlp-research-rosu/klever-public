requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports INT

  syntax Int ::= fibfibSpec(Int) [function, total, no-evaluators]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY
  imports INT
  imports BOOL

  // Mathematical FibFib sequence.  Concrete equations give the three bases
  // and the recurrence on every integer in its intended (nonnegative) domain.
  rule fibfibSpec(0) => 0 [concrete]
  rule fibfibSpec(1) => 0 [concrete]
  rule fibfibSpec(2) => 1 [concrete]
  rule fibfibSpec(N:Int)
    => fibfibSpec(N -Int 1) +Int fibfibSpec(N -Int 2) +Int fibfibSpec(N -Int 3)
    requires N >=Int 3
    [concrete]
  rule fibfibSpec(N:Int) => 0
    requires N <Int 0
    [concrete]

  // The loop advances the consecutive triple F(i), F(i+1), F(i+2).
  // This is the recurrence above with N = I + 3, oriented for the invariant.
  rule fibfibSpec(I:Int) +Int fibfibSpec(I +Int 1)
         +Int fibfibSpec(I +Int 2)
    => fibfibSpec(I +Int 3)
    requires I >=Int 0
    [simplification]
endmodule
