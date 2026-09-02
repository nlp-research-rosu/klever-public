requires "verification.k"

module REVIEWER-WRONG-SUMMARY
  imports MPY
  imports VERIFICATION-SYNTAX

  // Deliberately opposite interpretations, isolated from every positive build.
  rule sumInts(ACC:Int, _:ValSeq) => ACC +Int 42
  rule reverseSlice(VS:ValSeq) => VS
  rule sumToFloat(_:Int, vCons(F:Float, _:ValSeq)) => F
endmodule
