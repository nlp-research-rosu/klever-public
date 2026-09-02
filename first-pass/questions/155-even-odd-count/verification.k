// verification.k — proof scaffolding + summary functions, on the UNIFIED semantics.
// The symbolic input is presented as the opaque carrier intOfD(CS) (STR-INT-DECIMAL-LEMMAS):
// str(abs(intOfD(CS))) collapses to str(CS) via the bridge, then the loop folds CS. See
// ../../reference/notes/2026-07-07-str-int-bridge-design.md.

requires "../../reference/src/lemmas.k"

module EVEN-ODD-COUNT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so intOfD(CS) can be a Call arg).
  syntax Expr ::= Val

  // ---- digit-decomposition summaries = the spec (differential-tested vs CPython) ----
  // A digit char with code C has value (C - 48); it is EVEN iff (C - 48) % 2 == 0 — the
  // same floored-modInt parity test the body computes via `int(i) % 2 == 0`.  Both
  // accumulators thread through the loop-invariant scope, so the fold summaries are
  // [function, total] (see ../NOTES.md on scope-map values needing [total]).

  // evenDigit(C): the digit code C is even.  Matches the body's true-branch predicate.
  syntax Bool ::= evenDigit(Int) [function, total]
  rule evenDigit(C:Int) => (C -Int 48) modInt 2 ==Int 0 [simplification]

  // evenCnt(S, EC): running count EC plus the number of EVEN digits in S.
  // Branch-split on evenDigit(C) — the same test the body's If branches on.
  syntax Int ::= evenCnt(IntSeq, Int) [function, total]
  rule evenCnt(.IntSeq, EC:Int) => EC [simplification]
  rule evenCnt(iCons(C:Int, S:IntSeq), EC:Int)
    => evenCnt(S, EC +Int 1) requires evenDigit(C)         [simplification]
  rule evenCnt(iCons(C:Int, S:IntSeq), EC:Int)
    => evenCnt(S, EC)        requires notBool evenDigit(C) [simplification]

  // oddCnt(S, OC): running count OC plus the number of ODD digits in S (the else branch).
  syntax Int ::= oddCnt(IntSeq, Int) [function, total]
  rule oddCnt(.IntSeq, OC:Int) => OC [simplification]
  rule oddCnt(iCons(C:Int, S:IntSeq), OC:Int)
    => oddCnt(S, OC)        requires evenDigit(C)         [simplification]
  rule oddCnt(iCons(C:Int, S:IntSeq), OC:Int)
    => oddCnt(S, OC +Int 1) requires notBool evenDigit(C) [simplification]
endmodule
