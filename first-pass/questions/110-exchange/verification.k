requires "../../reference/src/lemmas.k"

module EXCHANGE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // the odd / even element counts of the int list
  syntax Int ::= countOdd(IntList) [function, total]
  rule countOdd(intListOf(.ValSeq)) => 0 [simplification]
  rule countOdd(intListOf(vCons(V:Val, S:ValSeq))) => 1 +Int countOdd(intListOf(S))
    requires isInt(V) andBool pyMod({V}:>Int, 2) ==Int 1
    [simplification]
  rule countOdd(intListOf(vCons(V:Val, S:ValSeq))) => countOdd(intListOf(S))
    requires isInt(V) andBool pyMod({V}:>Int, 2) =/=Int 1
    [simplification]

  syntax Int ::= countEven(IntList) [function, total]
  rule countEven(intListOf(.ValSeq)) => 0 [simplification]
  rule countEven(intListOf(vCons(V:Val, S:ValSeq))) => 1 +Int countEven(intListOf(S))
    requires isInt(V) andBool pyMod({V}:>Int, 2) ==Int 0
    [simplification]
  rule countEven(intListOf(vCons(V:Val, S:ValSeq))) => countEven(intListOf(S))
    requires isInt(V) andBool pyMod({V}:>Int, 2) =/=Int 0
    [simplification]
endmodule
