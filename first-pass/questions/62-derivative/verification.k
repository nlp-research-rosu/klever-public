// verification.k — summary for the derivative proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module DERIVATIVE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // derivFrom(VS, IDX) = position-dependent map: element V at index IDX contributes
  // IDX * V when IDX >= 1 (dropping the constant term at index 0). Order preserved.
  syntax ValSeq ::= derivFrom(ValSeq, Int) [function, total]
  rule derivFrom(.ValSeq, _:Int) => .ValSeq [simplification]
  rule derivFrom(vCons(V:Val, S:ValSeq), IDX:Int)
    => vCons(IDX *Int projectIntTotal(V), derivFrom(S, IDX +Int 1)) requires IDX >=Int 1 [simplification]
  rule derivFrom(vCons(V:Val, S:ValSeq), IDX:Int)
    => derivFrom(S, IDX +Int 1) requires notBool (IDX >=Int 1) [simplification]

endmodule
