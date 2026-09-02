requires "reference-semantics/semantics.k"

module FIBFIB-VERIFICATION
  imports MPY

  // fibFrom(A, B, C, N) is the first component after N shifts of
  // (A, B, C) -> (B, C, A + B + C).
  syntax Int ::= fibFrom(Int, Int, Int, Int) [function]
  rule fibFrom(A:Int, _B:Int, _C:Int, N:Int) => A
    requires N <=Int 0
  rule fibFrom(A:Int, B:Int, C:Int, N:Int)
    => fibFrom(B, C, A +Int B +Int C, N -Int 1)
    requires N >Int 0

  // Normalize the loop's incremented index to the form produced by the
  // recursive fibFrom equation.
  rule N:Int -Int (I:Int +Int 1) => N -Int I +Int -1 [simplification]
endmodule
