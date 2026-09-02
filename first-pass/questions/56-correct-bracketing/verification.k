// verification.k — summary for the correct_bracketing proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module CORRECT-BRACKETING-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // Decompose code-sequence equality so `b == "<"` (iCons(C,.) ==K iCons(40,.))
  // reduces to C ==Int 60 — a clean Int condition for the If to split on.

  // ---- summary ---- +1 per "(" (code 60), -1 otherwise.
  syntax Int ::= depthOf(IntSeq, Int) [function, total]
  rule depthOf(.IntSeq, D:Int)                 => D [simplification]
  rule depthOf(iCons(C:Int, S:IntSeq), D:Int)  => depthOf(S, D +Int 1) requires C  ==Int 60 [simplification]
  rule depthOf(iCons(C:Int, S:IntSeq), D:Int)  => depthOf(S, D -Int 1) requires C =/=Int 60 [simplification]

  // running depth (from D) drops below 0 at some step.
  syntax Bool ::= everNeg(IntSeq, Int) [function, total]
  rule everNeg(.IntSeq, _D:Int) => false [simplification]
  rule everNeg(iCons(C:Int, S:IntSeq), D:Int)
    => ((D +Int 1) <Int 0) orBool everNeg(S, D +Int 1) requires C  ==Int 60 [simplification]
  rule everNeg(iCons(C:Int, S:IntSeq), D:Int)
    => ((D -Int 1) <Int 0) orBool everNeg(S, D -Int 1) requires C =/=Int 60 [simplification]

  // balanced from depth D: never went negative AND ends at depth 0.
  syntax Bool ::= correctFrom(IntSeq, Int) [function, total]
  rule correctFrom(CS:IntSeq, D:Int)
    => (notBool everNeg(CS, D)) andBool (depthOf(CS, D) ==Int 0) [simplification]
endmodule
