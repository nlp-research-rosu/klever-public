// verification.k — proof scaffolding: a symbolic-input subsort and the summary
// function (the spec). On the UNIFIED semantics. See ../../NOTES.md.

requires "../../reference/src/lemmas.k"

module COUNT-DISTINCT-CHARACTERS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so str(CS) can be a Call arg).
  syntax Expr ::= Val

  // ---- summary function = the spec (differential-tested vs CPython: 0 mismatches) ----
  // count_distinct_characters(s) = len(set(s.lower())) = the number of DISTINCT codes after
  // lowercasing.  This is EXACTLY the composition the three builtins reduce to:
  //   .lower()  -> mapLower(CS)          (MPY-METHODS)
  //   set(...)  -> setV(dedupCodes(_))   (MPY-SET — the distinct codes)
  //   len(...)  -> isLen                 (MPY-BUILTINS: seqLen(setV(DS)) => isLen(DS))
  // So distinctCount(CS) is a thin name for isLen(dedupCodes(mapLower(CS))); the single
  // [simplification] rule lets the entry postcondition read distinctCount(CS) while unifying
  // with the term symbolic execution produces.  No induction: the program is a straight-line
  // nested expression, so each builtin fires once on the symbolic str(...)/setV(...) head.
  syntax Int ::= distinctCount(IntSeq) [function, total]
  rule distinctCount(CS:IntSeq) => isLen(dedupCodes(mapLower(CS))) [simplification]
endmodule
