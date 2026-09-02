requires "reference-semantics/semantics.k"

module DIGITS-VERIFICATION
  imports MPY

  // Product of the odd decimal digits of N, accumulated into A.  The value
  // zero is the implementation's sentinel for "no odd digit seen yet".
  syntax Int ::= oddDigitProduct(Int, Int) [function, total]
               | oddDigitStep(Bool, Int, Int, Int) [function, total]

  rule oddDigitProduct(0, A:Int) => A

  rule oddDigitProduct(N:Int, A:Int)
    => oddDigitStep(
         pyMod(N, 2) ==Int 1,
         (N -Int pyMod(N, 10)) /Int 10,
         pyMod(N, 10),
         A)
    requires N >Int 0

  rule oddDigitStep(B:Bool, Q:Int, _:Int, A:Int)
    => oddDigitProduct(Q, A)
    requires notBool B

  rule oddDigitStep(B:Bool, Q:Int, D:Int, 0)
    => oddDigitProduct(Q, D)
    requires B

  rule oddDigitStep(B:Bool, Q:Int, D:Int, A:Int)
    => oddDigitProduct(Q, A *Int D)
    requires B andBool A =/=Int 0

  // Target-side function equations are not re-fired automatically after the
  // symbolic execution learns a branch condition.  These three simplifiers
  // expose the same defining recurrence when the prover compares the
  // post-state of one loop iteration with the invariant's original state.
  rule {
    oddDigitProduct(
      (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10,
      A)
    #Equals
    oddDigitProduct(N, A)
  } => true
    requires N >Int 0
     andBool pyMod(N, 2) =/=Int 1
    [simplification]

  rule {
    oddDigitProduct(
      (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10,
      (N %Int 10 +Int 10) %Int 10)
    #Equals
    oddDigitProduct(N, 0)
  } => true
    requires N >Int 0
     andBool pyMod(N, 2) ==Int 1
    [simplification]

  rule {
    oddDigitProduct(
      (N -Int ((N %Int 10 +Int 10) %Int 10)) /Int 10,
      A *Int ((N %Int 10 +Int 10) %Int 10))
    #Equals
    oddDigitProduct(N, A)
  } => true
    requires N >Int 0
     andBool A =/=Int 0
     andBool pyMod(N, 2) ==Int 1
    [simplification]
endmodule
