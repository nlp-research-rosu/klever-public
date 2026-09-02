requires "reference-semantics/semantics.k"

module BRIDGE-BASE
  imports MPY

  // Same independently justified sort projection as the candidate, but with
  // no #iterNext bridge imported into this definition.
  syntax Int ::= intValue(Val) [function, total]
  rule intValue(I:Int) => I
endmodule
