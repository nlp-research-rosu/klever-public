// verification.k — summary for the `continue` proof

requires "../../../src/lemmas.k"

module LOOP-CONTINUE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val   // proof-only: a Val may sit in expression position

  syntax Int ::= posSum(ValSeq, Int) [function, total]
  rule posSum(.ValSeq, B:Int) => B [simplification]
  rule posSum(vCons(V:Val, S:ValSeq), B:Int)
    => #if projectIntTotal(V) <Int 0 #then posSum(S, B) #else posSum(S, B +Int projectIntTotal(V)) #fi
       [simplification]
endmodule
