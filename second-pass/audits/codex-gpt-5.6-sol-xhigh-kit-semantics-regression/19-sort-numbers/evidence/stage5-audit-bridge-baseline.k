requires "reference-semantics/semantics.k"

module AUDIT-BRIDGE-BASELINE
  imports MPY

  claim [empty]:
    <k> splitWS(
          joinCodes(iCons(32, .IntSeq), .ValSeq),
          .IntSeq,
          .ValSeq)
      => .ValSeq </k>

  claim [two-valid-words]:
    <k> splitWS(
          joinCodes(
            iCons(32, .IntSeq),
            vCons(str(strToCodes("one")),
              vCons(str(strToCodes("two")), .ValSeq))),
          .IntSeq,
          .ValSeq)
      => vCons(str(strToCodes("one")),
           vCons(str(strToCodes("two")), .ValSeq)) </k>

  claim [comma-actual-result]:
    <k> splitWS(
          joinCodes(
            iCons(44, .IntSeq),
            vCons(str(strToCodes("one")),
              vCons(str(strToCodes("two")), .ValSeq))),
          .IntSeq,
          .ValSeq)
      => vCons(str(strToCodes("one,two")), .ValSeq) </k>
endmodule
