requires "../../reference/src/lemmas.k"

module INTERSPERSE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // interleave D into VS; F is the loop's `first` flag (elements copied verbatim — any Val list)
  syntax ValSeq ::= interAcc(ValSeq, Val, Bool) [function, total]
  rule interAcc(.ValSeq, _D:Val, _F:Bool)             => .ValSeq [simplification]
  rule interAcc(vCons(N:Val, S:ValSeq), D:Val, true)  => vCons(N, interAcc(S, D, false)) [simplification]
  rule interAcc(vCons(N:Val, S:ValSeq), D:Val, false)
    => vCons(D, vCons(N, interAcc(S, D, false))) [simplification]

endmodule
