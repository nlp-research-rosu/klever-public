// verification.k — summary for the add_elements proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module ADD-ELEMENTS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // addEl(VS, IDX, K) = sum of the elements at index < K with at most two digits
  // (-9 <= x <= 99), folding from index IDX. Elements projected to Int.
  syntax Int ::= addEl(ValSeq, Int, Int) [function, total]
  rule addEl(.ValSeq, _:Int, _:Int) => 0 [simplification]
  rule addEl(vCons(V:Val, S:ValSeq), IDX:Int, K:Int)
    => projectIntTotal(V) +Int addEl(S, IDX +Int 1, K)
    requires IDX <Int K andBool projectIntTotal(V) >=Int -9 andBool projectIntTotal(V) <=Int 99 [simplification]
  rule addEl(vCons(V:Val, S:ValSeq), IDX:Int, K:Int)
    => addEl(S, IDX +Int 1, K)
    requires notBool (IDX <Int K andBool projectIntTotal(V) >=Int -9 andBool projectIntTotal(V) <=Int 99) [simplification]
endmodule
