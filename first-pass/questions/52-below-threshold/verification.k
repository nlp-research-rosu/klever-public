requires "../../reference/src/lemmas.k"

module BELOW-THRESHOLD-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // the recursive predicate: true iff every element of the int list is strictly below t
  syntax Bool ::= allBelow(IntList, Int) [function, total]
  rule allBelow(intListOf(.ValSeq), _T:Int) => true [simplification]
  rule allBelow(intListOf(vCons(V:Val, S:ValSeq)), T:Int)
    => ({V}:>Int <Int T) andBool allBelow(intListOf(S), T)
    requires isInt(V)
    [simplification]
endmodule
