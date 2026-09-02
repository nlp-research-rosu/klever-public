// verification.k — maximum on the UNIFIED semantics. sorted() is TRUSTED (mpy-sort.k);
// the result is the last k of the sorted input, `s[-k:]`, rebuilt by index as
// [ sorted(arr)[n-k+j] | j in range(0, k) ]. The sorted list is only INDEXED (valSeqAt,
// [total] so an opaque sort is defined), never iterated. The last-k index reconstruction
// is VERIFIED. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module MAXIMUM-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // maxFold(J, K, N, SS, ACC) = ACC ++ [ SS[n-k+j] | j in [J, K) ], indexing the sorted
  // sequence SS via valSeqAt (total) exactly as the program's subscript s[(n-k)+j] does.
  syntax ValSeq ::= maxFold(Int, Int, Int, ValSeq, ValSeq) [function, total]
  rule maxFold(J:Int, K:Int, _N:Int, _SS:ValSeq, ACC:ValSeq) => ACC requires J >=Int K [simplification]
  rule maxFold(J:Int, K:Int, N:Int, SS:ValSeq, ACC:ValSeq)
    => maxFold(J +Int 1, K, N, SS, valSeqConcat(ACC, vCons(valSeqAt(SS, normIdx((N -Int K) +Int J, vsLen(SS))), .ValSeq)))
    requires J <Int K [simplification]

  // result over the whole array: the last k of sorted(ARR).
  syntax Val ::= maximumRes(ValSeq, Int) [function]
  rule maximumRes(ARR:ValSeq, K:Int) => list(maxFold(0, K, vsLen(ARR), sortVS(ARR), .ValSeq)) [simplification]
endmodule
