// verification.k — anti_shuffle on the UNIFIED semantics, TRAP-FREE (W3 P86).
// solution.py is canonical verbatim; per-word ''.join(sorted(list(i))) lands
// as the composed shared atoms (charsOf/sortVS/joinCodes); the mapping
// comprehension folds via mapAcc; the sortstr helper and its trap are GONE.

requires "../../reference/src/lemmas.k"

module ANTI-SHUFFLE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // the mapping comp, threaded-accumulator style: each word appends its
  // sorted-characters string (the executed atom spelled verbatim)
  syntax ValSeq ::= mapAcc(ValSeq, ValSeq) [function, total, no-evaluators]
  rule mapAcc(.ValSeq, ACC:ValSeq) => ACC [simplification]
  rule mapAcc(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => mapAcc(R, valSeqConcat(ACC,
         vCons(str(joinCodes(.IntSeq, sortVS(charsOf(codesProj(V))))), .ValSeq)))
    [simplification]
endmodule
