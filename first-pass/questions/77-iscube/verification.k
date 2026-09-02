// verification.k — iscube on the UNIFIED semantics. cubeAcc has the #31 primeAcc shape: a
// sticky Bool set true if some r in [I, HI) satisfies r^3 == A (bounded scan). See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module ISCUBE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // cubeAcc(I, HI, A, F): F starts false; set true if any r in [I, HI) has r*r*r == A.
  syntax Bool ::= cubeAcc(Int, Int, Int, Bool) [function, total]
  rule cubeAcc(I:Int, HI:Int, _A:Int, F:Bool) => F requires I >=Int HI [simplification]
  rule cubeAcc(I:Int, HI:Int, A:Int, _F:Bool) => cubeAcc(I +Int 1, HI, A, true)
       requires I <Int HI andBool I *Int I *Int I ==Int A [simplification]
  rule cubeAcc(I:Int, HI:Int, A:Int, F:Bool) => cubeAcc(I +Int 1, HI, A, F)
       requires I <Int HI andBool I *Int I *Int I =/=Int A [simplification]
endmodule
