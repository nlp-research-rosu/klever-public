// verification.k — summary for the total_match proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module TOTAL-MATCH-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // totalLen(VS) = sum of the string lengths in VS.
  syntax Int ::= totalLen(ValSeq) [function, total]
  rule totalLen(.ValSeq) => 0 [simplification]
  rule totalLen(vCons(V:Val, S:ValSeq)) => isLen(codesProj(V)) +Int totalLen(S) [simplification]
endmodule
