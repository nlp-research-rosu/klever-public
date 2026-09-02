requires "../../reference/src/lemmas.k"

module SUM-PRODUCT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // sum and product of the int list (empty sum 0, empty product 1)
  syntax Int ::= sumSeq(IntList) [function, total]
  rule sumSeq(intListOf(.ValSeq)) => 0 [simplification]
  rule sumSeq(intListOf(vCons(V:Val, S:ValSeq))) => {V}:>Int +Int sumSeq(intListOf(S))
    requires isInt(V)
    [simplification]

  syntax Int ::= prodSeq(IntList) [function, total]
  rule prodSeq(intListOf(.ValSeq)) => 1 [simplification]
  rule prodSeq(intListOf(vCons(V:Val, S:ValSeq))) => {V}:>Int *Int prodSeq(intListOf(S))
    requires isInt(V)
    [simplification]
endmodule
