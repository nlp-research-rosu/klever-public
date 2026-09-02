// verification.k — cycpattern_check on the UNIFIED semantics, TRAP-FREE
// (P154). solution.py rewrites the canonical early-return nested scan into a
// Bool-ACCUMULATOR scan (`found`): the inner/outer loops fold `found` via a
// guarded case-split on the raw window-equality atom — the is_prime primeAcc
// rung, nested (see is-prime-rung / nested-loop-rung). No early return, so no
// frame-pop and no competing FOUND/NOT-FOUND loop claims (which merged and bred
// a spurious min-over-float ghost branch under the old premise-split shape).
// The slices ride the SHARED doSlice/take-after-drop route; the window-equality
// guard is spelled INLINE as the raw takeIS/dropIS ==K atom so it is
// syntactically identical to the executed If condition (a winAt(...) wrapper
// would need kore to expand it during guard checking, which it does not).

requires "../../reference/src/lemmas.k"

module CYCPATTERN-CHECK-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // inner accumulator fold over j in [J, JHI): found := F, then per step set
  // found=True iff the window a[i:i+l] == pat[j:j+l]. Guarded case-split on the
  // raw ==K atom (matching the executed If), not orBool (kore folds guards).
  syntax Bool ::= foundJ(IntSeq, IntSeq, Int, Int, Int, Int, Bool) [function, total]
  rule foundJ(_AS:IntSeq, _PS:IntSeq, _I:Int, J:Int, JHI:Int, _L:Int, F:Bool) => F
    requires J >=Int JHI [simplification]
  rule foundJ(AS:IntSeq, PS:IntSeq, I:Int, J:Int, JHI:Int, L:Int, _F:Bool)
    => foundJ(AS, PS, I, J +Int 1, JHI, L, true)
    requires J <Int JHI andBool takeIS(dropIS(AS, I), L) ==K takeIS(dropIS(PS, J), L) [simplification]
  rule foundJ(AS:IntSeq, PS:IntSeq, I:Int, J:Int, JHI:Int, L:Int, F:Bool)
    => foundJ(AS, PS, I, J +Int 1, JHI, L, F)
    requires J <Int JHI andBool notBool (takeIS(dropIS(AS, I), L) ==K takeIS(dropIS(PS, J), L)) [simplification]

  // outer accumulator fold over i in [I, IHI): each step runs the inner fold
  // (seeded j in [0, JHI)) threading `found`; guarded on I<IHI.
  syntax Bool ::= foundI(IntSeq, IntSeq, Int, Int, Int, Int, Bool) [function, total]
  rule foundI(_AS:IntSeq, _PS:IntSeq, I:Int, IHI:Int, _JHI:Int, _L:Int, F:Bool) => F
    requires I >=Int IHI [simplification]
  rule foundI(AS:IntSeq, PS:IntSeq, I:Int, IHI:Int, JHI:Int, L:Int, F:Bool)
    => foundI(AS, PS, I +Int 1, IHI, JHI, L, foundJ(AS, PS, I, 0, JHI, L, F))
    requires I <Int IHI [simplification]

  // the whole result over pat = b + b, seed found=false
  syntax Bool ::= cycRes(IntSeq, IntSeq) [function]
  rule cycRes(AS:IntSeq, BS:IntSeq)
    => foundI(AS, seqConcat(BS, BS), 0, isLen(AS) -Int isLen(BS) +Int 1, isLen(BS) +Int 1, isLen(BS), false)
    [simplification]
endmodule
