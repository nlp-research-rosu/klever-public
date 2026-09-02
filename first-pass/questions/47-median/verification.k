// verification.k — median (odd-length) on the UNIFIED semantics. sorted() is TRUSTED
// (mpy-sort.k: opaque sortVS symbolic, concrete for krun). The straight-line index
// s[len//2] = valSeqAt(sortVS(VS), vsLen(VS)/2) stays an abstract term matching the
// postcondition — no summary/ordering lemma; the trust is discharged by the diff-test.
// See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module MEDIAN-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val
endmodule
