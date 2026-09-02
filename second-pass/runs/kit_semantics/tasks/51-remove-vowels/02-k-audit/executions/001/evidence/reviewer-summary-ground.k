requires "verification.k"

module REVIEWER-SUMMARY-GROUND
  imports VERIFICATION

  claim [empty]:
    <k> removeVowelsFrom(.IntSeq, .IntSeq)
        => .IntSeq
    </k>

  claim [vowel-a]:
    <k> removeVowelsFrom(iCons(97, .IntSeq), .IntSeq)
        => .IntSeq
    </k>

  claim [consonant-b]:
    <k> removeVowelsFrom(iCons(98, .IntSeq), .IntSeq)
        => iCons(98, .IntSeq)
    </k>

  claim [mixed-bA-z]:
    <k>
      removeVowelsFrom(
        iCons(98, iCons(65, iCons(45, iCons(122, .IntSeq)))),
        .IntSeq)
      => iCons(98, iCons(45, iCons(122, .IntSeq)))
    </k>
endmodule
