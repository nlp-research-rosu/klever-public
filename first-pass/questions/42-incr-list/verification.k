requires "../../reference/src/lemmas.k"

module INCR-LIST-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // map (+1) over the int list, order and length preserved
  syntax ValSeq ::= incrVS(IntList) [function, total]
  rule incrVS(intListOf(.ValSeq)) => .ValSeq [simplification]
  rule incrVS(intListOf(vCons(V:Val, S:ValSeq)))
    => vCons({V}:>Int +Int 1, incrVS(intListOf(S)))
    requires isInt(V)
    [simplification]

endmodule
