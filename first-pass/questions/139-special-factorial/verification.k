// verification.k — summary for the special_factorial proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module SPECIAL-FACTORIAL-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- summary functions = the spec (the two COUPLED accumulators) -----------
  // The loop body at index I is:  fact_i = fact_i * I;  special_fact = special_fact * fact_i.
  // Folding indices I, I+1, ..., HI-1 starting from (fact_i=F, special_fact=S):
  //
  //   facFold(I, HI, F)     = value of fact_i      after those iterations.
  //   sfacFold(I, HI, F, S) = value of special_fact after those iterations.
  //
  // sfacFold is COUPLED to fact_i: each step special_fact *= the NEW fact_i (= F*I),
  // so sfacFold threads the running fact_i F alongside S.  For the entry the loop
  // runs I = 1..n with (F=1, S=1), so special_fact ends = 1!*2!*...*n! (super factorial).
  //
  // [total]: both summaries land in the <scopes> scope as values, so each must be total
  // (a partial helper there can taint Map:in_keys to \bottom and abort the prover —
  // NOTES).  The two rules of each are exhaustive on I (I >=Int HI / I <Int HI).
  // Python `*` on ints is exact => *Int.
  syntax Int ::= facFold(Int, Int, Int)      [function, total]
               | sfacFold(Int, Int, Int, Int) [function, total]

  rule facFold(I:Int, HI:Int, F:Int) => F                              requires I >=Int HI [simplification]
  rule facFold(I:Int, HI:Int, F:Int) => facFold(I +Int 1, HI, F *Int I) requires I <Int HI  [simplification]

  rule sfacFold(I:Int, HI:Int, _F:Int, S:Int) => S                                          requires I >=Int HI [simplification]
  rule sfacFold(I:Int, HI:Int, F:Int, S:Int)  => sfacFold(I +Int 1, HI, F *Int I, S *Int (F *Int I)) requires I <Int HI [simplification]
endmodule
