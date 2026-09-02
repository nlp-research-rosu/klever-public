// verification.k — summary for the is_simple_power proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module IS-SIMPLE-POWER-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- summary function = the spec (the GROWING while loop) ----------------
  // powUp(P, N, X) = the final value of `power` after running
  //     while P < X: P = P * N
  // starting from `power = P`.  This is the exact recurrence the while loop realizes —
  // each iteration replaces power by power*N, and the loop stops once power >= X.
  //   powUp(P, N, X) = P                      if P >= X   (loop stops immediately)
  //   powUp(P, N, X) = powUp(P*N, N, X)       if P <  X   (one body pass, then re-loop)
  // Branch-split on `P <Int X` — the SAME split the loop condition `while power < x` makes.
  // [total] because it lands in the loop-invariant's scope-map value (NOTES.md: a partial
  // there can crash the prover via in_keys ... \bottom).  The two rules are exhaustive
  // (P >= X or P < X).
  //
  // Result spec: is_simple_power(X, N) = (N == 1 ? X == 1 : powUp(1, N, X) == X).
  // For N >= 2 and X >= 1 this is exactly "EXISTS k >= 0 with N**k == X" (the loop walks
  // 1, N, N^2, ... up to the first value >= X and tests equality).  Differential-tested
  // vs the canonical (0 / 500k random positive pairs) — see PROOF.md.
  syntax Int ::= powUp(Int, Int, Int) [function, total]
  rule powUp(P:Int, _N:Int, X:Int) => P                    requires P >=Int X  [simplification]
  rule powUp(P:Int,  N:Int, X:Int) => powUp(P *Int N, N, X) requires P <Int  X  [simplification]
endmodule
