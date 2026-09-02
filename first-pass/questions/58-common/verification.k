// verification.k — common on the UNIFIED semantics. sorted(list(set(...))) intersection is
// rewritten as a single loop over l1 that keeps each e1 that is in l2 and not already collected,
// then sorted(). The intersect+dedup is VERIFIED; the sort is the trusted sortVS.
//
// Both `e1 in l2` (l2 a fixed symbolic list) and `e1 not in out` (out the symbolic accumulator)
// ride the REAL <k>-cell #memberAcc fold, reduced by the SHARED faithful lemma
// (lemmas/list.k) to the defined total memberVS — the same ==K-leaved value the
// fold computes. commonFold case-splits on the combined guard.

requires "../../reference/src/lemmas.k"

module COMMON-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // commonFold(l1remaining, l2, accOut) = accOut + the first occurrences of l1 elements that are in
  // l2 (order preserved). Case-splits on `memberVS(X, L2) andBool notBool memberVS(X, OUT)`.
  syntax ValSeq ::= commonFold(ValSeq, ValSeq, ValSeq) [function, total]
  rule commonFold(.ValSeq, _L2:ValSeq, OUT:ValSeq) => OUT [simplification]
  rule commonFold(vCons(X:Val, R:ValSeq), L2:ValSeq, OUT:ValSeq)
    => commonFold(R, L2, valSeqConcat(OUT, vCons(X, .ValSeq)))
       requires memberVS(X, L2) andBool notBool memberVS(X, OUT) [simplification]
  rule commonFold(vCons(X:Val, R:ValSeq), L2:ValSeq, OUT:ValSeq)
    => commonFold(R, L2, OUT)
       requires notBool (memberVS(X, L2) andBool notBool memberVS(X, OUT)) [simplification]

endmodule
