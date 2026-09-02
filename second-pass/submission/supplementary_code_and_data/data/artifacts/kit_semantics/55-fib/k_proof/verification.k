requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports INT

  // The first component after N applications of
  // (A, B) |-> (B, A + B).  The N <= 0 branch totalizes the helper;
  // proof claims use it only for N >= 0.
  syntax Int ::= fibFrom(Int, Int, Int) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX
  imports INT
  imports BOOL

  rule fibFrom(A, _B, N) => A
    requires N <=Int 0

  rule fibFrom(A, B, N) => fibFrom(B, A +Int B, N -Int 1)
    requires N >Int 0

  rule (A:Int +Int B:Int) -Int A => B [simplification]
endmodule
