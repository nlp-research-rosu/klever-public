// verification.k — strange_sort_list on the UNIFIED semantics. sorted() is TRUSTED (mpy-sort.k);
// the result reads the sorted list alternately from both ends: position i takes s[i//2] (even i)
// or s[n-1-i//2] (odd i). The sorted list is only INDEXED (valSeqAt, now [total] so an opaque
// sort is defined), never iterated. The index-reconstruction is VERIFIED. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module STRANGE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // reconFoldV(I, N, SS, ACC) = ACC ++ [ SS[i//2] if i even else SS[n-1-i//2] | i in [I, N) ],
  // indexing the sorted sequence SS via valSeqAt (total) exactly as the program's subscript does.
  syntax ValSeq ::= reconFoldV(Int, Int, ValSeq, ValSeq) [function, total]
  rule reconFoldV(I:Int, N:Int, _SS:ValSeq, ACC:ValSeq) => ACC requires I >=Int N [simplification]
  rule reconFoldV(I:Int, N:Int, SS:ValSeq, ACC:ValSeq)
    => reconFoldV(I +Int 1, N, SS, valSeqConcat(ACC, vCons(valSeqAt(SS, normIdx(I /Int 2, vsLen(SS))), .ValSeq)))
    requires I <Int N andBool I %Int 2 ==Int 0 [simplification]
  rule reconFoldV(I:Int, N:Int, SS:ValSeq, ACC:ValSeq)
    => reconFoldV(I +Int 1, N, SS, valSeqConcat(ACC, vCons(valSeqAt(SS, normIdx(N -Int 1 -Int (I /Int 2), vsLen(SS))), .ValSeq)))
    requires I <Int N andBool I %Int 2 =/=Int 0 [simplification]

  // result over the whole list: reconstruct from sorted(LST).
  syntax Val ::= strangeRes(ValSeq) [function]
  rule strangeRes(LST:ValSeq) => list(reconFoldV(0, vsLen(LST), sortVS(LST), .ValSeq)) [simplification]
endmodule
