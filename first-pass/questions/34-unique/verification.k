// verification.k — unique on the UNIFIED semantics. sorted(list(set(l))) is rewritten as an
// order-preserving dedup loop `for x in l: if x not in out: out = out + [x]` then sorted(out)
// (behaviorally identical — both yield the sorted distinct elements). The DEDUP is VERIFIED; the
// sort is the trusted sortVS.
//
// KEY construct: `x not in out` reads the SYMBOLIC accumulator `out`. The
// membership rides the REAL <k>-cell fold, reduced by the SHARED FAITHFUL
// lemma (lemmas/list.k) to the defined total memberVS — the same ==K-leaved
// value the fold computes; opaque on symbolic VS, so `dedupFold` case-splits
// on it. krun runs the real fold, so the smoke exercises the actual dedup.

requires "../../reference/src/lemmas.k"

module UNIQUE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // dedupFold(remaining, acc) = acc extended with the first occurrences in `remaining`.
  syntax ValSeq ::= dedupFold(ValSeq, ValSeq) [function, total]
  rule dedupFold(.ValSeq, OUT:ValSeq) => OUT [simplification]
  rule dedupFold(vCons(X:Val, R:ValSeq), OUT:ValSeq) => dedupFold(R, OUT)
       requires memberVS(X, OUT) [simplification]
  rule dedupFold(vCons(X:Val, R:ValSeq), OUT:ValSeq) => dedupFold(R, valSeqConcat(OUT, vCons(X, .ValSeq)))
       requires notBool memberVS(X, OUT) [simplification]

endmodule
