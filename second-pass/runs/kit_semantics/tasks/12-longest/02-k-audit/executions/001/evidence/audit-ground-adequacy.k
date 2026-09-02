requires "verification.k"

module AUDIT-GROUND-ADEQUACY
  imports VERIFICATION

  claim [empty-contract-value]:
    <k> longestValue(.ValSeq) => noneV </k>

  claim [nonempty-contract-value]:
    <k>
      longestValue(
        vCons(
          str(iCons(97, .IntSeq)),
          vCons(
            str(iCons(98, iCons(98, .IntSeq))),
            vCons(str(iCons(99, .IntSeq)), .ValSeq)
          )
        )
      )
      => str(iCons(98, iCons(98, .IntSeq)))
    </k>

  claim [loop-summary-value]:
    <k>
      scanLongest(
        vCons(
          str(iCons(98, iCons(98, .IntSeq))),
          vCons(str(iCons(99, .IntSeq)), .ValSeq)
        ),
        str(iCons(97, .IntSeq))
      )
      => str(iCons(98, iCons(98, .IntSeq)))
    </k>

  claim [entry-guards-satisfied]:
    <k>
      isStringValue(str(iCons(97, .IntSeq)))
      andBool allStrings(
        vCons(
          str(iCons(98, iCons(98, .IntSeq))),
          vCons(str(iCons(99, .IntSeq)), .ValSeq)
        )
      )
      => true
    </k>
endmodule
