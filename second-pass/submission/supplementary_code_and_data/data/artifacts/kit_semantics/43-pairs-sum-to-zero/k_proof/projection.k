requires "reference-semantics/semantics.k"

module INT-PROJECTION
  imports MPY

  // A total, guarded sort projection.  The non-Int value is irrelevant to the
  // proof bridges, whose domain requires isInt(V), but makes totality explicit.
  syntax Int ::= intProj(Val) [function, total]
  rule intProj(I:Int) => I
  rule intProj(V:Val) => 0
    requires notBool isInt(V)
endmodule
