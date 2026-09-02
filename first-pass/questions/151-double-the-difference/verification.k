requires "../../reference/src/lemmas.k"

module DOUBLE-DIFF-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // the contribution of E: E*E when E is a positive odd integer, else 0
  syntax Int ::= contrib(Int) [function, total]
  rule contrib(E:Int) => E *Int E
    requires E >Int 0 andBool pyMod(E, 2) ==Int 1 [simplification]
  rule contrib(E:Int) => 0
    requires notBool (E >Int 0 andBool pyMod(E, 2) ==Int 1) [simplification]

  // the sum of contributions over the int list
  syntax Int ::= ddiff(IntList) [function, total]
  rule ddiff(intListOf(.ValSeq)) => 0 [simplification]
  rule ddiff(intListOf(vCons(V:Val, S:ValSeq))) => contrib({V}:>Int) +Int ddiff(intListOf(S))
    requires isInt(V)
    [simplification]
endmodule
