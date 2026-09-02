// verification.k — summary for the smallest_change proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module SMALLEST-CHANGE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // revAcc(S, R) = S reversed, prepended onto R (the pass-1 `rev = [x] + rev` fold).
  syntax ValSeq ::= revAcc(ValSeq, ValSeq) [function, total]
  rule revAcc(.ValSeq, R:ValSeq)                => R                        [simplification]
  rule revAcc(vCons(V:Val, S:ValSeq), R:ValSeq) => revAcc(S, vCons(V, R))   [simplification]

  // zipMismatch(S1, S2, CNT) = CNT plus the number of aligned positions where the two lists
  // differ (stopping at the shorter). Branch-split on the int comparison (a-r != 0),
  // matching pass-2 `if a != r: cnt += 1`.
  syntax Int ::= zipMismatch(ValSeq, ValSeq, Int) [function, total]
  rule zipMismatch(.ValSeq, _S2:ValSeq, CNT:Int)              => CNT [simplification]
  rule zipMismatch(vCons(_:Val, _:ValSeq), .ValSeq, CNT:Int)  => CNT [simplification]
  rule zipMismatch(vCons(X:Val, R1:ValSeq), vCons(Y:Val, R2:ValSeq), CNT:Int)
    => zipMismatch(R1, R2, CNT +Int 1) requires projectIntTotal(X) =/=Int projectIntTotal(Y) [simplification]
  rule zipMismatch(vCons(X:Val, R1:ValSeq), vCons(Y:Val, R2:ValSeq), CNT:Int)
    => zipMismatch(R1, R2, CNT)         requires projectIntTotal(X) ==Int projectIntTotal(Y) [simplification]

  // revAcc only permutes elements, so it preserves allInt — needed to discharge the zip
  // loop's `allInt(S2)` precondition on rev = revAcc(A, .ValSeq).
  rule allInt(revAcc(S:ValSeq, R:ValSeq)) => allInt(S) andBool allInt(R) [simplification]
endmodule
