// verification.k — summary for the is_happy proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module IS-HAPPY-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // happyFold(CS, IDX, P1, P2, H) = the happy flag after folding CS from index IDX with
  // previous two codes P1 (i-1) and P2 (i-2). From IDX>=2, three consecutive not-distinct
  // (code==P1 or P1==P2 or code==P2) clears H. Codes come from ord (no projection).
  syntax Bool ::= happyFold(IntSeq, Int, Int, Int, Bool) [function, total]
  rule happyFold(.IntSeq, _:Int, _:Int, _:Int, H:Bool) => H [simplification]
  rule happyFold(iCons(C:Int, S:IntSeq), IDX:Int, P1:Int, P2:Int, _H:Bool)
    => happyFold(S, IDX +Int 1, C, P1, false)
    requires IDX >=Int 2 andBool (C ==Int P1 orBool P1 ==Int P2 orBool C ==Int P2) [simplification]
  rule happyFold(iCons(C:Int, S:IntSeq), IDX:Int, P1:Int, P2:Int, H:Bool)
    => happyFold(S, IDX +Int 1, C, P1, H)
    requires notBool (IDX >=Int 2 andBool (C ==Int P1 orBool P1 ==Int P2 orBool C ==Int P2)) [simplification]
endmodule
