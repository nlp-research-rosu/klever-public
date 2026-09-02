// verification.k — summary for the modp proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module MODP-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // modIter(N, R, P) = the value of `ret` after N iterations of `ret = 2*ret % p` from
  // ret = R. Equals (2^N * R) mod P; for entry R = 1 it is 2^N mod P (the modp spec).
  // Python `%` is the reference's pyMod (floored). [total]: exhaustive on N (<=0 / >0).
  syntax Int ::= modIter(Int, Int, Int) [function, total]
  rule modIter(N:Int, R:Int, _P:Int) => R                                        requires N <=Int 0 [simplification]
  rule modIter(N:Int, R:Int, P:Int)  => modIter(N -Int 1, pyMod(2 *Int R, P), P)  requires N >Int 0  [simplification]

  // Normalize the range step's count so the circularity's modIter argument unifies:
  // rangeObj(I+1, N, 1) yields N -Int (I +Int 1); the invariant unfold yields N -Int I -Int 1.
endmodule
