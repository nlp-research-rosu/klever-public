requires "../../reference/src/lemmas.k"

module SUM-SQUARES-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // the contribution of element E at index I: i%3==0 -> E^2 ; elif i%4==0 -> E^3 ; else E
  syntax Int ::= transform(Int, Int) [function, total]
  rule transform(E:Int, I:Int) => E *Int E
    requires pyMod(I, 3) ==Int 0 [simplification]
  rule transform(E:Int, I:Int) => E *Int E *Int E
    requires pyMod(I, 3) =/=Int 0 andBool pyMod(I, 4) ==Int 0 [simplification]
  rule transform(E:Int, I:Int) => E
    requires pyMod(I, 3) =/=Int 0 andBool pyMod(I, 4) =/=Int 0 [simplification]

  // the sum of transformed elements from index I
  syntax Int ::= sumSq(IntList, Int) [function, total]
  rule sumSq(intListOf(.ValSeq), _I:Int) => 0 [simplification]
  rule sumSq(intListOf(vCons(V:Val, S:ValSeq)), I:Int)
    => transform({V}:>Int, I) +Int sumSq(intListOf(S), I +Int 1)
    requires isInt(V)
    [simplification]
endmodule
