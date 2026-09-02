requires "verification.k"

module SPEC-GROUND-SUMMARY
  imports VERIFICATION

  // "cat" at the actual entry iterator position I = 0 must summarize to
  // "catac" (99,97,116,97,99).
  claim
    <k>
      palindromeFrom(
        iCons(99, iCons(97, iCons(116, .IntSeq))),
        0)
      =>
      iCons(99, iCons(97, iCons(116, iCons(97, iCons(99, .IntSeq)))))
    </k>

endmodule
