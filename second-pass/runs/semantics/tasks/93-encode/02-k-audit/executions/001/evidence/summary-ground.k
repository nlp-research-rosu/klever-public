requires "verification.k"

module SUMMARY-GROUND
  imports ENCODE-VERIFICATION

  claim [empty-summary]:
    <k>
      encodeCodes(.IntSeq)
      =>
      .IntSeq
    </k>

  claim [test-summary]:
    <k>
      encodeCodes(
        iCons(116, iCons(101, iCons(115, iCons(116, .IntSeq)))))
      =>
      iCons(84, iCons(71, iCons(83, iCons(84, .IntSeq))))
    </k>

  claim [loop-accumulator-summary]:
    <k>
      encodeAcc(
        iCons(116, iCons(101, iCons(115, iCons(116, .IntSeq)))),
        iCons(80, .IntSeq))
      =>
      iCons(80, iCons(84, iCons(71, iCons(83, iCons(84, .IntSeq)))))
    </k>

  claim [vowel-branch]:
    <k>
      encodeCode(101)
      =>
      71
    </k>

  claim [consonant-branch]:
    <k>
      encodeCode(98)
      =>
      66
    </k>
endmodule
