requires "../../reference/src/lemmas.k"

module BELOW-ZERO-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // the recursive predicate: true iff the running sum of the int list ever goes negative
  syntax Bool ::= wentNeg(IntList, Int) [function, total]
  rule wentNeg(intListOf(.ValSeq), _B:Int) => false [simplification]
  rule wentNeg(intListOf(vCons(V:Val, S:ValSeq)), B:Int)
    => (B +Int {V}:>Int <Int 0) orBool wentNeg(intListOf(S), B +Int {V}:>Int)
    requires isInt(V)
    [simplification]
endmodule
