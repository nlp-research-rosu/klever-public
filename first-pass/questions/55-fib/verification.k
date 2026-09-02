// verification.k — proof scaffolding: a symbolic-input subsort and the summary
// functions (the spec). On the UNIFIED semantics. See ../46-fib4/, ../24-largest-divisor/,
// ../../NOTES.md.

requires "../../reference/src/lemmas.k"

module FIB-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so a symbolic Int can be a
  // Call argument).
  syntax Expr ::= Val

  // ---- the sliding 2-window (the loop's state) -------------------------------
  // The loop keeps two scalars (a, b).  One iteration does `a, b = b, a + b`, sliding
  // the window to [b, a+b].  winA/winB(K, A, B) are the two components AFTER K such
  // slides from the seed (A, B).  [total] (they land in the <scopes> scope map).  The
  // new value MUST be the program's exact `a + b` = A +Int B so the circularity closes
  // syntactically.  (2-accumulator analog of 46-fib4's fibA-D; see NOTES.)
  syntax Int ::= winA(Int, Int, Int) [function, total]
               | winB(Int, Int, Int) [function, total]
  rule winA(K:Int, A:Int, _B:Int) => A requires K <=Int 0 [simplification]
  rule winB(K:Int, _A:Int, B:Int) => B requires K <=Int 0 [simplification]
  rule winA(K:Int, A:Int, B:Int) => winA(K -Int 1, B, A +Int B) requires K >Int 0 [simplification]
  rule winB(K:Int, A:Int, B:Int) => winB(K -Int 1, B, A +Int B) requires K >Int 0 [simplification]

  // ---- the whole answer ------------------------------------------------------
  // fibOf(N) = winA(N, 0, 1): the first window component after N slides from the seed
  // [0, 1] (range(N) runs N times).  For N<=0 this is winA(K<=0)=A=0 (fib(0)=0).
  // Differential-tested vs canonical fib.
  syntax Int ::= fibOf(Int) [function, total]
  rule fibOf(N:Int) => winA(N, 0, 1) [simplification]

  // count normalization: the loop invariant's remaining count is HI - I; re-applying
  // the circularity at start I+1 yields HI - (I+1), which must line up with the step
  // rule's (HI - I) - 1.  (See NOTES / unified-range-loop-invariant.)
endmodule
