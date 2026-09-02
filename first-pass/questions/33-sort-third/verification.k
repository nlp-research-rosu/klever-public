// verification.k — sort_third on the UNIFIED semantics. Sort the elements at indices divisible by 3;
// leave the rest. solution.py GATHERS the stride-3 elements, `sorted()`s them (TRUSTED, mpy-sort.k),
// then INTERLEAVE-builds the answer by indexing the sorted list at the divisible-by-3 positions and
// the original list elsewhere. Composes the trusted-sort rung (sortVS, indexed via valSeqAt) + two
// range-loop folds (the Q70 fresh-sorted-list pattern) — no new reference feature. The gather/filter,
// the index reconstruction, and the interleave are VERIFIED; only the sort ORDER is trusted. See
// ./PROOF.md.

requires "../../reference/src/lemmas.k"

module SORT-THIRD-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // strideFold(K, N, VS, ACC) = ACC ++ [ l[k] | k in [K,N), k%3==0 ] — the stride-3 gather.
  syntax ValSeq ::= strideFold(Int, Int, ValSeq, ValSeq) [function, total]
  rule strideFold(K:Int, N:Int, _VS:ValSeq, ACC:ValSeq) => ACC requires K >=Int N [simplification]
  rule strideFold(K:Int, N:Int, VS:ValSeq, ACC:ValSeq)
    => strideFold(K +Int 1, N, VS, valSeqConcat(ACC, vCons(valSeqAt(VS, K), .ValSeq)))
    requires K <Int N andBool pyMod(K, 3) ==Int 0 [simplification]
  rule strideFold(K:Int, N:Int, VS:ValSeq, ACC:ValSeq)
    => strideFold(K +Int 1, N, VS, ACC)
    requires K <Int N andBool pyMod(K, 3) =/=Int 0 [simplification]

  // buildFold(I, N, VS, ST, ACC) = ACC ++ [ ST[i//3] if i%3==0 else l[i] | i in [I,N) ] — the
  // interleave. ST is the sorted stride list, indexed at i//3 (= (i - i%3)/3, the reference's //).
  syntax ValSeq ::= buildFold(Int, Int, ValSeq, ValSeq, ValSeq) [function, total]
  rule buildFold(I:Int, N:Int, _VS:ValSeq, _ST:ValSeq, ACC:ValSeq) => ACC requires I >=Int N [simplification]
  rule buildFold(I:Int, N:Int, VS:ValSeq, ST:ValSeq, ACC:ValSeq)
    => buildFold(I +Int 1, N, VS, ST, valSeqConcat(ACC, vCons(valSeqAt(ST, (I -Int pyMod(I, 3)) /Int 3), .ValSeq)))
    requires I <Int N andBool pyMod(I, 3) ==Int 0 [simplification]
  rule buildFold(I:Int, N:Int, VS:ValSeq, ST:ValSeq, ACC:ValSeq)
    => buildFold(I +Int 1, N, VS, ST, valSeqConcat(ACC, vCons(valSeqAt(VS, I), .ValSeq)))
    requires I <Int N andBool pyMod(I, 3) =/=Int 0 [simplification]

endmodule
