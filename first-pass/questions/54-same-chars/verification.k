// verification.k — proof scaffolding: a symbolic-input subsort and the summary
// function (the spec). On the UNIFIED semantics. See ../../NOTES.md.

requires "../../reference/src/lemmas.k"

module SAME-CHARS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so str(CS) can be a Call arg).
  syntax Expr ::= Val

  // ---- summary function = the spec (differential-tested vs CPython: 0 mismatches) ----
  // same_chars(s0, s1) = set(s0) == set(s1) = the two strings consist of the same SET of
  // characters.  This is EXACTLY the composition the builtins reduce to (MPY-SET):
  //   set(s0) -> setV(dedupCodes(CS0))
  //   set(s1) -> setV(dedupCodes(CS1))
  //   ==      -> sameSet(_, _) = subsetCodes both directions
  // So sameChars(CS0, CS1) is a thin name for sameSet(dedupCodes(CS0), dedupCodes(CS1)); the
  // single [simplification] rule lets the entry postcondition read sameChars(CS0, CS1) while
  // unifying with the term symbolic execution produces.  No induction — the program is a
  // straight-line nested expression, so each builtin fires once on the symbolic head.
  syntax Bool ::= sameChars(IntSeq, IntSeq) [function, total]
  rule sameChars(CS0:IntSeq, CS1:IntSeq)
    => sameSet(dedupCodes(CS0), dedupCodes(CS1)) [simplification]
endmodule
