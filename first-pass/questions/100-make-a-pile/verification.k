// verification.k — summary for the make_a_pile proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module MAKE-A-PILE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // pileV(I, N, B) = the length-max(N,0) ValSeq whose k-th element (k = 0..N-1) is
  // B + 2*(I+k) — i.e. [B + 2*i for i in rangeObj(I, N, 1)]. For the entry (I=0, B=N)
  // element i = N + 2*i (the spec). Head B +Int (2 *Int I) matches `n + 2*i`. [total].
  syntax ValSeq ::= pileV(Int, Int, Int) [function, total]
  rule pileV(_I:Int, N:Int, _B:Int) => .ValSeq                                            requires N <=Int 0 [simplification]
  rule pileV(I:Int, N:Int, B:Int)   => vCons(B +Int (2 *Int I), pileV(I +Int 1, N -Int 1, B)) requires N >Int 0 [simplification]

  // Right-cons accumulator lemmas ($acc = $acc + [e]) + range count normalization.
endmodule
