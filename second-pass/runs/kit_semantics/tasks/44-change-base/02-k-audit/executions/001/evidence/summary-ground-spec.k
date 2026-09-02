requires "verification.k"

module SUMMARY-GROUND-SPEC
  imports VERIFICATION

  claim [positive]:
    changeBaseCodes(8, 3)
    =>
    iCons(50, iCons(50, .IntSeq))

  claim [zero]:
    changeBaseCodes(0, 2)
    =>
    iCons(48, .IntSeq)

  claim [negative]:
    changeBaseCodes(-8, 3)
    =>
    iCons(45, iCons(50, iCons(50, .IntSeq)))
endmodule
