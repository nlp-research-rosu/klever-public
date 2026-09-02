requires "connection-verification.k"

module ADD-ELEMENTS-CONNECTION-FOUNDATION-SPEC
  imports ADD-ELEMENTS-CONNECTION-VERIFICATION

  claim [concat-length]:
    <k>
      vsLen(valSeqConcat(PREFIX:ValSeq, SUFFIX:ValSeq))
      =>
      vsLen(PREFIX) +Int vsLen(SUFFIX)
      ...
    </k>

  claim [length-nonnegative]:
    <k>
      vsLen(VALUES:ValSeq) >=Int 0
      =>
      true
      ...
    </k>
endmodule
