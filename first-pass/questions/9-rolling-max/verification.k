requires "../../reference/src/lemmas.k"

module ROLLING-MAX-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // provenance marker
  syntax IntList ::= intListOf(ValSeq)

  // the list of running maxima; M is the current running max, F the `first` flag
  syntax ValSeq ::= rollAcc(IntList, Val, Bool) [function, total]
  rule rollAcc(intListOf(.ValSeq), _M:Val, _F:Bool)              => .ValSeq [simplification]
  rule rollAcc(intListOf(vCons(V:Val, S:ValSeq)), _M:Val, true)  => vCons(V, rollAcc(intListOf(S), V, false)) [simplification]
  rule rollAcc(intListOf(vCons(V:Val, S:ValSeq)), M:Val, false)
    => vCons(V, rollAcc(intListOf(S), V, false))
    requires isInt(V) andBool isInt(M) andBool {V}:>Int >Int {M}:>Int
    [simplification]
  rule rollAcc(intListOf(vCons(V:Val, S:ValSeq)), M:Val, false)
    => vCons(M, rollAcc(intListOf(S), M, false))
    requires isInt(V) andBool isInt(M) andBool {V}:>Int <=Int {M}:>Int
    [simplification]

endmodule
