// verification.k — sort_even on the UNIFIED semantics. Sort the even-index elements, leave the odd
// ones. Identical rung to sort_third (#33) at stride 2: GATHER the even-index elements, `sorted()`
// them (TRUSTED, mpy-sort.k), then INTERLEAVE-build indexing the sorted list at even positions and
// the original elsewhere. Composes the trusted-sort rung (sortVS, indexed via valSeqAt, Q70 fresh-
// sorted pattern) + two range-loop folds — no new feature. Gather/interleave/index VERIFIED; sort
// order trusted. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module SORT-EVEN-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // strideFold(K, N, VS, ACC) = ACC ++ [ l[k] | k in [K,N), k%2==0 ] — the even-index gather.
  syntax ValSeq ::= strideFold(Int, Int, ValSeq, ValSeq) [function, total]
  rule strideFold(K:Int, N:Int, _VS:ValSeq, ACC:ValSeq) => ACC requires K >=Int N [simplification]
  rule strideFold(K:Int, N:Int, VS:ValSeq, ACC:ValSeq)
    => strideFold(K +Int 1, N, VS, valSeqConcat(ACC, vCons(valSeqAt(VS, K), .ValSeq)))
    requires K <Int N andBool pyMod(K, 2) ==Int 0 [simplification]
  rule strideFold(K:Int, N:Int, VS:ValSeq, ACC:ValSeq)
    => strideFold(K +Int 1, N, VS, ACC)
    requires K <Int N andBool pyMod(K, 2) =/=Int 0 [simplification]

  // buildFold(I, N, VS, ST, ACC) = ACC ++ [ ST[i//2] if i%2==0 else l[i] | i in [I,N) ] — interleave.
  syntax ValSeq ::= buildFold(Int, Int, ValSeq, ValSeq, ValSeq) [function, total]
  rule buildFold(I:Int, N:Int, _VS:ValSeq, _ST:ValSeq, ACC:ValSeq) => ACC requires I >=Int N [simplification]
  rule buildFold(I:Int, N:Int, VS:ValSeq, ST:ValSeq, ACC:ValSeq)
    => buildFold(I +Int 1, N, VS, ST, valSeqConcat(ACC, vCons(valSeqAt(ST, (I -Int pyMod(I, 2)) /Int 2), .ValSeq)))
    requires I <Int N andBool pyMod(I, 2) ==Int 0 [simplification]
  rule buildFold(I:Int, N:Int, VS:ValSeq, ST:ValSeq, ACC:ValSeq)
    => buildFold(I +Int 1, N, VS, ST, valSeqConcat(ACC, vCons(valSeqAt(VS, I), .ValSeq)))
    requires I <Int N andBool pyMod(I, 2) =/=Int 0 [simplification]

endmodule
