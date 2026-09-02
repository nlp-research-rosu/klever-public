// verification.k — starts_one_ends on the UNIFIED semantics. Closed form: the count of n-digit
// positive integers starting or ending with 1 is 1 for n==1, else 18*10^(n-2). No loop.
//
// The blocker is the SYMBOLIC power `10 ** (n-2)`: kprove reasoning about
// `^Int` with a symbolic exponent HANGS (nonlinear). The SHARED ipow lemma
// (lemmas/arith.k) keeps the power as an opaque atom; krun computes the real
// power. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module STARTS-ONE-ENDS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // soe(n) = #n-digit positive integers starting or ending with 1. Domain n >= 1 (positive int, per
  // the prompt). The two guards partition the domain (n==1 | n>=2); [simplification] so each fires
  // under the program's own `if n==1` split and matches the (now opaque-ipow) computed term.
  syntax Int ::= soe(Int) [function]
  rule soe(N:Int) => 1                          requires N ==Int 1 [simplification]
  rule soe(N:Int) => 18 *Int ipow(10, N -Int 2) requires N >=Int 2 [simplification]
endmodule
