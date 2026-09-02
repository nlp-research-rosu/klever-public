// verification.k — summary for the prod_signs proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module PROD-SIGNS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  syntax Int ::= absOf(Int) [function, total]
  rule absOf(X:Int) => 0 -Int X requires X  <Int 0 [simplification]
  rule absOf(X:Int) => X        requires X >=Int 0 [simplification]
  syntax Int ::= sumAbs(ValSeq) [function, total]
  rule sumAbs(.ValSeq) => 0 [simplification]
  rule sumAbs(vCons(V:Val, S:ValSeq)) => absOf(projectIntTotal(V)) +Int sumAbs(S) [simplification]

  syntax Int ::= signOf(Int) [function, total]
  rule signOf(X:Int) => -1 requires X  <Int 0 [simplification]
  rule signOf(X:Int) => 0  requires X ==Int 0 [simplification]
  rule signOf(X:Int) => 1  requires X  >Int 0 [simplification]
  syntax Int ::= signProd(ValSeq) [function, total]
  rule signProd(.ValSeq) => 1 [simplification]
  rule signProd(vCons(V:Val, S:ValSeq)) => signOf(projectIntTotal(V)) *Int signProd(S) [simplification]
endmodule
