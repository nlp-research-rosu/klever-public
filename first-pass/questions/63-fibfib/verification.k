// verification.k — proof scaffolding: a symbolic-input subsort and the summary
// functions (the spec). On the UNIFIED semantics. See ../55-fib/, ../46-fib4/,
// ../../NOTES.md.

requires "../../reference/src/lemmas.k"

module FIBFIB-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so a symbolic Int can be a
  // Call argument).
  syntax Expr ::= Val

  // ---- the sliding 3-window (the loop's state) -------------------------------
  // The loop keeps three scalars (a, b, c).  One iteration does `a, b, c = b, c,
  // a + b + c`, sliding the window to [b, c, (a+b)+c].  winA/winB/winC(K, A,B,C) are
  // the three components AFTER K such slides from the seed (A,B,C).  [total] (they land
  // in the <scopes> scope map).  The new value MUST be the program's exact `a + b + c` =
  // (A +Int B) +Int C so the circularity closes syntactically.  (3-accumulator analog of
  // 55-fib / 46-fib4; see NOTES.)
  syntax Int ::= winA(Int, Int, Int, Int) [function, total]
               | winB(Int, Int, Int, Int) [function, total]
               | winC(Int, Int, Int, Int) [function, total]
  rule winA(K:Int, A:Int, _B:Int, _C:Int) => A requires K <=Int 0 [simplification]
  rule winB(K:Int, _A:Int, B:Int, _C:Int) => B requires K <=Int 0 [simplification]
  rule winC(K:Int, _A:Int, _B:Int, C:Int) => C requires K <=Int 0 [simplification]
  rule winA(K:Int, A:Int, B:Int, C:Int) => winA(K -Int 1, B, C, (A +Int B) +Int C) requires K >Int 0 [simplification]
  rule winB(K:Int, A:Int, B:Int, C:Int) => winB(K -Int 1, B, C, (A +Int B) +Int C) requires K >Int 0 [simplification]
  rule winC(K:Int, A:Int, B:Int, C:Int) => winC(K -Int 1, B, C, (A +Int B) +Int C) requires K >Int 0 [simplification]

  // ---- the whole answer ------------------------------------------------------
  // fibfibOf(N) = winA(N, 0, 0, 1): the first window component after N slides from the
  // seed [0, 0, 1] (range(N) runs N times).  For N<=0 this is winA(K<=0)=A=0.
  // Differential-tested vs canonical fibfib.
  syntax Int ::= fibfibOf(Int) [function, total]
  rule fibfibOf(N:Int) => winA(N, 0, 0, 1) [simplification]

  // count normalization (cf. NOTES / unified-range-loop-invariant).
endmodule
