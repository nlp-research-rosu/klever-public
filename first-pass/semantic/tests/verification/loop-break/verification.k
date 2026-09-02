// verification.k — summary for the `break` proof

requires "../../../src/lemmas.k"

module LOOP-BREAK-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val   // proof-only: a Val may sit in expression position

  syntax Int ::= prefixSum(ValSeq, Int) [function, total]
  rule prefixSum(.ValSeq, B:Int) => B [simplification]
  rule prefixSum(vCons(V:Val, S:ValSeq), B:Int)
    => #if projectIntTotal(V) <Int 0 #then B #else prefixSum(S, B +Int projectIntTotal(V)) #fi
       [simplification]
endmodule
