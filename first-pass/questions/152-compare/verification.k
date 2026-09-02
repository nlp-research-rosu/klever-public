requires "../../reference/src/lemmas.k"

module COMPARE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // element-wise |x - y| over the zipped int lists, stopping at the shorter
  syntax ValSeq ::= compareVS(IntList, IntList) [function, total]
  rule compareVS(intListOf(.ValSeq), _:IntList) => .ValSeq [simplification]
  rule compareVS(intListOf(vCons(_:Val, _:ValSeq)), intListOf(.ValSeq)) => .ValSeq [simplification]
  rule compareVS(intListOf(vCons(X:Val, S1:ValSeq)), intListOf(vCons(Y:Val, S2:ValSeq)))
    => vCons(absInt({X}:>Int -Int {Y}:>Int), compareVS(intListOf(S1), intListOf(S2)))
    requires isInt(X) andBool isInt(Y)
    [simplification]

endmodule
