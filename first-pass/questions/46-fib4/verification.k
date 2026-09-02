// verification.k — proof scaffolding: a symbolic-input subsort and the summary
// functions (the spec). On the UNIFIED semantics. See ../24-largest-divisor/,
// ../60-sum-to-n/, ../../NOTES.md.

requires "../../reference/src/lemmas.k"

module FIB4-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL   // the #if _ #then _ #else _ #fi used in fib4Of's base

  // proof-only: let a Val sit in expression position (so a symbolic Int can be a
  // Call argument).
  syntax Expr ::= Val

  // ---- the sliding 4-window (the loop's state) -------------------------------
  // The loop keeps four scalars (a, b, c, d) = a 4-window. One iteration does the
  // tuple-unpack `a, b, c, d = b, c, d, a + b + c + d`, sliding the window to
  // [b, c, d, ((a+b)+c)+d].  fibA/B/C/D(K, A,B,C,D) are the four components AFTER K
  // such slides from the seed (A,B,C,D).  All [total] (they land in the <scopes>
  // scope map; see NOTES "[total]").  The new value MUST be ((A +Int B) +Int C) +Int D
  // — the program's exact left-nested `a + b + c + d` association — so the
  // circularity closes syntactically.
  syntax Int ::= fibA(Int, Int, Int, Int, Int) [function, total]
               | fibB(Int, Int, Int, Int, Int) [function, total]
               | fibC(Int, Int, Int, Int, Int) [function, total]
               | fibD(Int, Int, Int, Int, Int) [function, total]
  rule fibA(K:Int, A:Int, _B:Int, _C:Int, _D:Int) => A requires K <=Int 0 [simplification]
  rule fibB(K:Int, _A:Int, B:Int, _C:Int, _D:Int) => B requires K <=Int 0 [simplification]
  rule fibC(K:Int, _A:Int, _B:Int, C:Int, _D:Int) => C requires K <=Int 0 [simplification]
  rule fibD(K:Int, _A:Int, _B:Int, _C:Int, D:Int) => D requires K <=Int 0 [simplification]
  rule fibA(K:Int, A:Int, B:Int, C:Int, D:Int) => fibA(K -Int 1, B, C, D, ((A +Int B) +Int C) +Int D) requires K >Int 0 [simplification]
  rule fibB(K:Int, A:Int, B:Int, C:Int, D:Int) => fibB(K -Int 1, B, C, D, ((A +Int B) +Int C) +Int D) requires K >Int 0 [simplification]
  rule fibC(K:Int, A:Int, B:Int, C:Int, D:Int) => fibC(K -Int 1, B, C, D, ((A +Int B) +Int C) +Int D) requires K >Int 0 [simplification]
  rule fibD(K:Int, A:Int, B:Int, C:Int, D:Int) => fibD(K -Int 1, B, C, D, ((A +Int B) +Int C) +Int D) requires K >Int 0 [simplification]

  // ---- the whole answer ------------------------------------------------------
  // fib4Of(N) = [0,0,2,0][N] for N<4 (= 2 if N==2 else 0, the early-return value),
  // else fibD(N-3, 0,0,2,0): the LAST window component after N-3 slides from the seed
  // [0,0,2,0] (range(4, N+1) runs N-3 times).  Differential-tested vs canonical.
  syntax Int ::= fib4Of(Int) [function, total]
  rule fib4Of(N:Int) => #if N ==Int 2 #then 2 #else 0 #fi requires N <Int 4  [simplification]
  rule fib4Of(N:Int) => fibD(N -Int 3, 0, 0, 2, 0)        requires N >=Int 4 [simplification]

  // count normalization: the loop invariant's remaining count is HI - I; when the
  // circularity is re-applied at the next start I+1 it yields HI - (I+1), which must
  // line up with the step rule's (HI - I) - 1.  (See NOTES / unified-range-loop-invariant.)
endmodule
