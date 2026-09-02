requires "base-verification.k"

module FIXED-LEMMA-SPEC
  imports BASE-VERIFICATION

  claim [concat-associative]:
    <k>
      valSeqConcat(valSeqConcat(A, B), C)
      =>
      valSeqConcat(A, valSeqConcat(B, C))
    </k>

  claim [concat-right-identity]:
    <k>
      valSeqConcat(A, .ValSeq)
      =>
      A
    </k>
endmodule
