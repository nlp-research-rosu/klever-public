// verification.k — summary for the `x in list` fold proof (the <k>-cell iterNext
// membership fold narrows a symbolic list, like all/any).

requires "../../../src/lemmas.k"

module MEMBER-FOLD-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // structural membership — the SAME branch shape as memberAcc/memberCont
  // (mpy-operators): found on head-match, else recurse. (A single orBool rule
  // does not reduce cleanly under the fold's branch condition.)
  syntax Bool ::= memberOf(Val, ValSeq) [function, total]
  rule memberOf(_V:Val, .ValSeq)               => false        [simplification]
  rule memberOf(V:Val, vCons(E:Val, _S:ValSeq)) => true        requires E ==K V           [simplification]
  rule memberOf(V:Val, vCons(E:Val, S:ValSeq))  => memberOf(V, S) requires notBool (E ==K V) [simplification]
endmodule
