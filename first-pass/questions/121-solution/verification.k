requires "../../reference/src/lemmas.k"

module ODD-AT-EVEN-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // the contribution of element E at index I: E when I is even and E is odd, else 0
  syntax Int ::= contrib(Int, Int) [function, total]
  rule contrib(E:Int, I:Int) => E
    requires pyMod(I, 2) ==Int 0 andBool pyMod(E, 2) ==Int 1 [simplification]
  rule contrib(E:Int, I:Int) => 0
    requires notBool (pyMod(I, 2) ==Int 0 andBool pyMod(E, 2) ==Int 1) [simplification]

  // the sum of contributions from index I
  syntax Int ::= sumOE(IntList, Int) [function, total]
  rule sumOE(intListOf(.ValSeq), _I:Int) => 0 [simplification]
  rule sumOE(intListOf(vCons(V:Val, S:ValSeq)), I:Int)
    => contrib({V}:>Int, I) +Int sumOE(intListOf(S), I +Int 1)
    requires isInt(V)
    [simplification]
endmodule
