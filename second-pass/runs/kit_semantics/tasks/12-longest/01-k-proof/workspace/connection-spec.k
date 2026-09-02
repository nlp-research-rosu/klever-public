requires "verification.k"

module CONNECTION-SPEC
  imports VERIFICATION-BASE

  // Bridge-free, universal connection over the complete canonical Str domain.
  claim [string-length-connection]:
    <k>
      seqLen(str(CS:IntSeq))
      => seqLenString(str(CS))
    </k>

  claim [string-projection-connection]:
    <k>
      projectString(str(CS:IntSeq))
      => str(CS)
    </k>
endmodule
