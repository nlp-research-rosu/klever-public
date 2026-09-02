// verification.k — summary for the can_arrange proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module CAN-ARRANGE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // canArrFrom(VS, IDX, PV, ID) = the largest descent index after folding VS from index
  // IDX, previous value PV (a raw Val), current answer ID. Branch-splits on
  // (IDX>=1 andBool x<prev), matching the nested If.
  syntax Int ::= canArrFrom(ValSeq, Int, Val, Int) [function, total]
  rule canArrFrom(.ValSeq, _:Int, _:Val, ID:Int) => ID [simplification]
  rule canArrFrom(vCons(V:Val, CS:ValSeq), IDX:Int, PV:Val, _ID:Int)
    => canArrFrom(CS, IDX +Int 1, V, IDX)
    requires IDX >=Int 1 andBool projectIntTotal(V) <Int projectIntTotal(PV) [simplification]
  rule canArrFrom(vCons(V:Val, CS:ValSeq), IDX:Int, PV:Val, ID:Int)
    => canArrFrom(CS, IDX +Int 1, V, ID)
    requires notBool (IDX >=Int 1 andBool projectIntTotal(V) <Int projectIntTotal(PV)) [simplification]

  // prev accumulator: last element of VS (or PV if empty).
  syntax Val ::= lastOfV(ValSeq, Val) [function, total]
  rule lastOfV(.ValSeq, PV:Val)            => PV [simplification]
  rule lastOfV(vCons(V:Val, S:ValSeq), _:Val) => lastOfV(S, V) [simplification]
endmodule
