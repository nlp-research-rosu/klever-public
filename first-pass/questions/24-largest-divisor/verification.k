// verification.k — summary for the largest_divisor proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module LARGEST-DIVISOR-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- summary function = the spec (differential-tested vs canonical.py: 0/18k) --
  // lastDiv(N, I, HI, R) = the value of `result` after scanning index i = I, I+1,
  // ..., HI-1 (ASCENDING, half-open [I, HI)), starting from result = R, applying
  // `if n % i == 0: result = i` at each step.  Because the scan ascends and updates
  // on EVERY divisor, the final R is the LARGEST i in [I, HI) dividing N, or the
  // initial R if none divides.  For the entry I = 1, HI = N, R = 1 this is the
  // largest i in [1, N) with N % i == 0 (= the largest proper divisor of N), with
  // R = 1 as the floor (handles N prime, whose only in-range divisor is 1).
  //
  // The two recursive rules split on EXACTLY the loop body's branch
  // (n % i == 0) — same `requires` as the body's `If` — so under the path
  // condition each loop step reduces lastDiv(N,I,HI,R) to exactly the state the
  // body produces (cf. 35-max-element's maxFold and 31-is-prime's noDiv; NOTES
  // "Branch-split summaries to match the program's case-split").
  //
  // [total]: the three rules are exhaustive (I >=Int HI / I <Int HI x ==0/=/=0);
  // lastDiv lands as a <scopes> scope-map value in the loop-invariant RHS, and a
  // partial summary there can taint Map:in_keys to \bottom and abort the prover
  // (NOTES "Scope-map summary values must be [total]").  Python `%` is FLOORED =>
  // modInt, never %Int.
  syntax Int ::= lastDiv(Int, Int, Int, Int) [function, total]
  rule lastDiv(_N:Int, I:Int, HI:Int, R:Int) => R
       requires I >=Int HI [simplification]
  rule lastDiv(N:Int, I:Int, HI:Int, _R:Int) => lastDiv(N, I +Int 1, HI, I)
       requires I <Int HI andBool pyMod(N, I) ==Int 0 [simplification]
  rule lastDiv(N:Int, I:Int, HI:Int, R:Int) => lastDiv(N, I +Int 1, HI, R)
       requires I <Int HI andBool pyMod(N, I) =/=Int 0 [simplification]
endmodule
