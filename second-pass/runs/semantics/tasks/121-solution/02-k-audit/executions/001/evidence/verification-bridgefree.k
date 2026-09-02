requires "reference-semantics/semantics.k"

module VERIFICATION-BRIDGEFREE
  imports MPY

  // Same projection equation as the candidate, but none of the three
  // operational BinOp bridge rules are imported here.
  syntax Int ::= intProjection(Val) [function, total]
  rule intProjection(I:Int) => I
endmodule
