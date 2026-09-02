requires "../../reference/src/lemmas.k"

module CORRECT-BRACKETING-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // the running depth: +1 per "(" (code 40), -1 otherwise
  syntax Int ::= depthOf(IntSeq, Int) [function, total]
  rule depthOf(.IntSeq, D:Int)                 => D [simplification]
  rule depthOf(iCons(C:Int, S:IntSeq), D:Int)  => depthOf(S, D +Int 1) requires C  ==Int 40 [simplification]
  rule depthOf(iCons(C:Int, S:IntSeq), D:Int)  => depthOf(S, D -Int 1) requires C =/=Int 40 [simplification]

  // true iff the running depth (from D) ever drops below 0
  syntax Bool ::= everNeg(IntSeq, Int) [function, total]
  rule everNeg(.IntSeq, _D:Int) => false [simplification]
  rule everNeg(iCons(C:Int, S:IntSeq), D:Int)
    => ((D +Int 1) <Int 0) orBool everNeg(S, D +Int 1) requires C  ==Int 40 [simplification]
  rule everNeg(iCons(C:Int, S:IntSeq), D:Int)
    => ((D -Int 1) <Int 0) orBool everNeg(S, D -Int 1) requires C =/=Int 40 [simplification]

  // balanced from depth D: never negative and ends at 0
  syntax Bool ::= correctFrom(IntSeq, Int) [function, total]
  rule correctFrom(CS:IntSeq, D:Int)
    => (notBool everNeg(CS, D)) andBool (depthOf(CS, D) ==Int 0) [simplification]
endmodule
