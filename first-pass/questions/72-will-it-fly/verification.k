// verification.k — summary for the will_it_fly proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module WILL-IT-FLY-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // sumVS(VS) = sum of the (projected) elements.
  syntax Int ::= sumVS(ValSeq) [function, total]
  rule sumVS(.ValSeq) => 0 [simplification]
  rule sumVS(vCons(V:Val, S:ValSeq)) => projectIntTotal(V) +Int sumVS(S) [simplification]

  // revVS(VS, R) = reverse(VS) prepended to R (raw Vals; the loop does rev = [x] + rev).
  syntax ValSeq ::= revVS(ValSeq, ValSeq) [function, total]
  rule revVS(.ValSeq, R:ValSeq) => R [simplification]
  rule revVS(vCons(V:Val, S:ValSeq), R:ValSeq) => revVS(S, vCons(V, R)) [simplification]
endmodule
