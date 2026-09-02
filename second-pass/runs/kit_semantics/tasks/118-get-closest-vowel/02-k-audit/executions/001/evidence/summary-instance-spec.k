requires "verification.k"

module SUMMARY-INSTANCE-SPEC
  imports VERIFICATION

  // CS = "bab"; the entry precondition is satisfied by a concrete MPY string.
  claim [bab-summary]:
    <k>
      closestVowel(
        iCons(98, iCons(97, iCons(98, .IntSeq))))
      =>
      iCons(97, .IntSeq)
    </k>

  // CS = "yogurt".
  claim [yogurt-summary]:
    <k>
      closestVowel(
        iCons(121,
        iCons(111,
        iCons(103,
        iCons(117,
        iCons(114,
        iCons(116, .IntSeq)))))))
      =>
      iCons(117, .IntSeq)
    </k>

  // CS = ""; exercises the lower-length boundary.
  claim [empty-summary]:
    <k> closestVowel(.IntSeq) => .IntSeq </k>

  // CS = "quick"; contains vowels, but none between two consonants.
  claim [quick-summary]:
    <k>
      closestVowel(
        iCons(113,
        iCons(117,
        iCons(105,
        iCons(99,
        iCons(107, .IntSeq))))))
      =>
      .IntSeq
    </k>
endmodule
