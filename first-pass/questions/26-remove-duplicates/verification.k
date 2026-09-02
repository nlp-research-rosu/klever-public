// verification.k — remove_duplicates on the UNIFIED semantics. Keep the elements that occur EXACTLY
// once (order preserved). The canonical uses collections.Counter (external lib); solution.py rewrites
// it as an INDEX-based nested double loop (behaviorally identical — diff-tested 0 mismatches): for
// each i, count how many j have numbers[j]==numbers[i], and append numbers[i] iff that count is 1.
//
// This composes two established rungs: the ELEMENT-COMPARE isInt bridge (the Q43 pairs_sum allInt
// applyBin echo, here for applyCmp "==") to reduce numbers[j]==numbers[i] on symbolic elements, and
// the LIST-BUILD fold (the Q34 unique dedupFold valSeqConcat accumulator) for the outer result. The
// count is fully VERIFIED (real fold, not trusted). See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module REMOVE-DUPLICATES-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- inner count fold over j in [J, N): c := c + #{ j : numbers[j] == numbers[i] } (i fixed).
  // Guarded case-split rules (the primeAcc/#31 pattern) — the guard is the If condition
  // numbers[j]==numbers[i] inlined (after the echo reduces it), so each branch discharges its rule.
  syntax Int ::= countEq(Int, Int, Int, ValSeq, Int) [function, total]
  rule countEq(J:Int, N:Int, _I:Int, _VS:ValSeq, C:Int) => C requires J >=Int N [simplification]
  rule countEq(J:Int, N:Int, I:Int, VS:ValSeq, C:Int) => countEq(J +Int 1, N, I, VS, C +Int 1)
    requires J <Int N andBool projectIntTotal(valSeqAt(VS, J)) ==Int  projectIntTotal(valSeqAt(VS, I)) [simplification]
  rule countEq(J:Int, N:Int, I:Int, VS:ValSeq, C:Int) => countEq(J +Int 1, N, I, VS, C)
    requires J <Int N andBool projectIntTotal(valSeqAt(VS, J)) =/=Int projectIntTotal(valSeqAt(VS, I)) [simplification]

  // ---- outer fold over i in [I, N): append numbers[i] to the result list iff its whole-list count
  // is exactly 1. The guard countEq(0, N, I, VS, 0) == 1 stays an opaque symbolic Int for symbolic
  // VS/N (the inner fold can't concretize), so the outer case-splits on `== 1` — matching the
  // program's `if c == 1`. Builds a ValSeq via valSeqConcat (the Q34 list-accumulator shape).
  syntax ValSeq ::= dupFilter(Int, Int, ValSeq, ValSeq) [function]
  rule dupFilter(I:Int, N:Int, _VS:ValSeq, R:ValSeq) => R requires I >=Int N [simplification]
  rule dupFilter(I:Int, N:Int, VS:ValSeq, R:ValSeq)
    => dupFilter(I +Int 1, N, VS, valSeqConcat(R, vCons(valSeqAt(VS, I), .ValSeq)))
    requires I <Int N andBool countEq(0, N, I, VS, 0) ==Int  1 [simplification]
  rule dupFilter(I:Int, N:Int, VS:ValSeq, R:ValSeq)
    => dupFilter(I +Int 1, N, VS, R)
    requires I <Int N andBool countEq(0, N, I, VS, 0) =/=Int 1 [simplification]

endmodule
