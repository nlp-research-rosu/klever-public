requires "verification.k"

module SUMMARY-MUTATION
  imports MPY
  imports VERIFICATION-SYNTAX

  // Deliberately wrong interpretations used only by negative probes.
  rule sumInts(_:Int, _:ValSeq) => 0
  rule sumToFloat(_:Int, vCons(V:Val, _:ValSeq))
    => projectFloatTotal(V)
    requires isFloat(V)
  rule reverseSlice(_:ValSeq) => .ValSeq
endmodule
