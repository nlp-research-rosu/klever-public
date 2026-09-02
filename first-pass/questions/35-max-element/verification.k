requires "../../reference/src/lemmas.k"

module MAX-ELEMENT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)


  // the running max of the int list from seed M; strict `>` keeps the earlier element on ties
  syntax Int ::= maxFold(IntList, Int) [function, total]
  rule maxFold(intListOf(.ValSeq), M:Int) => M [simplification]
  rule maxFold(intListOf(vCons(V:Val, S:ValSeq)), M:Int) => maxFold(intListOf(S), {V}:>Int)
    requires isInt(V) andBool {V}:>Int >Int M
    [simplification]
  rule maxFold(intListOf(vCons(V:Val, S:ValSeq)), M:Int) => maxFold(intListOf(S), M)
    requires isInt(V) andBool {V}:>Int <=Int M
    [simplification]
endmodule
