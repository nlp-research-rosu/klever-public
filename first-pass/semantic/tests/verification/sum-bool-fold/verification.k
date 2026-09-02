// verification.k — sum over a symbolic List[bool] (counts the Trues). Proves the
// intOf element rule narrows a symbolic bool list, mirroring the List[int] proof.

requires "../../../src/lemmas.k"

module SUM-BOOL-FOLD-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // matches sumAcc via intOf -> (isBool lemma) -> #if projectBoolTotal(V) then 1 else 0.
  syntax Int ::= countTrue(ValSeq, Int) [function, total]
  rule countTrue(.ValSeq, ACC:Int) => ACC [simplification]
  rule countTrue(vCons(V:Val, S:ValSeq), ACC:Int)
    => countTrue(S, ACC +Int #if projectBoolTotal(V) #then 1 #else 0 #fi) [simplification]
endmodule
