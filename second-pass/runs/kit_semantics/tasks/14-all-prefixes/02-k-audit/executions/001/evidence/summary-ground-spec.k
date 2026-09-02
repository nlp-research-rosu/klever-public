requires "verification.k"

module SUMMARY-GROUND-SPEC
  imports VERIFICATION

  claim [prefixes-abc]:
    prefixesAcc(
      .IntSeq,
      iCons(97, iCons(98, iCons(99, .IntSeq))),
      .ValSeq)
    =>
    vCons(
      str(iCons(97, .IntSeq)),
      vCons(
        str(iCons(97, iCons(98, .IntSeq))),
        vCons(
          str(iCons(97, iCons(98, iCons(99, .IntSeq)))),
          .ValSeq)))
endmodule
