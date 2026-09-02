requires "../../reference/src/lemmas.k"

module GET-POSITIVE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // the sublist of strictly-positive elements, order preserved
  syntax ValSeq ::= filterPos(IntList) [function, total]
  rule filterPos(intListOf(.ValSeq)) => .ValSeq [simplification]
  rule filterPos(intListOf(vCons(V:Val, S:ValSeq))) => vCons(V, filterPos(intListOf(S)))
    requires isInt(V) andBool {V}:>Int >Int 0
    [simplification]
  rule filterPos(intListOf(vCons(V:Val, S:ValSeq))) => filterPos(intListOf(S))
    requires isInt(V) andBool {V}:>Int <=Int 0
    [simplification]

endmodule
