requires "verification.k"

module GROUND-SUMMARY-SPEC
  imports ANTI-SHUFFLE-BASE

  // empty
  claim <k>
    antiShuffleSpec(.IntSeq)
    =>
    str(.IntSeq)
  </k>

  // "ba" -> "ab"
  claim <k>
    antiShuffleSpec(iCons(98, iCons(97, .IntSeq)))
    =>
    str(iCons(97, iCons(98, .IntSeq)))
  </k>

  // " a" -> " a" (empty first field)
  claim <k>
    antiShuffleSpec(iCons(32, iCons(97, .IntSeq)))
    =>
    str(iCons(32, iCons(97, .IntSeq)))
  </k>

  // "  ba  dc " -> "  ab  cd "
  claim <k>
    antiShuffleSpec(
      iCons(32, iCons(32, iCons(98, iCons(97,
      iCons(32, iCons(32, iCons(100, iCons(99, iCons(32, .IntSeq))))))))))
    =>
    str(
      iCons(32, iCons(32, iCons(97, iCons(98,
      iCons(32, iCons(32, iCons(99, iCons(100, iCons(32, .IntSeq))))))))))
  </k>
endmodule
