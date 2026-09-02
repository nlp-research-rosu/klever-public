requires "verification.k"

module AUDIT-WITNESS
  imports VERIFICATION

  claim [precondition-valid]:
    <k>
      validAlgebraLists(
        vCons(2, vCons(3, vCons(4, vCons(5, .ValSeq)))),
        valSeqConcat(
          vCons(
            str(iCons(43, .IntSeq)),
            vCons(
              str(iCons(42, .IntSeq)),
              vCons(str(iCons(45, .IntSeq)), .ValSeq))),
          vCons(str(.IntSeq), .ValSeq)))
      => true
    </k>

  claim [precondition-nonempty]:
    <k>
      notBool (
        vCons(
          str(iCons(43, .IntSeq)),
          vCons(
            str(iCons(42, .IntSeq)),
            vCons(str(iCons(45, .IntSeq)), .ValSeq)))
        ==K .ValSeq)
      => true
    </k>

  claim [summary-codes]:
    <k>
      runPairCodes(
        .IntSeq,
        vCons(2, vCons(3, vCons(4, vCons(5, .ValSeq)))),
        valSeqConcat(
          vCons(
            str(iCons(43, .IntSeq)),
            vCons(
              str(iCons(42, .IntSeq)),
              vCons(str(iCons(45, .IntSeq)), .ValSeq))),
          vCons(str(.IntSeq), .ValSeq)))
      =>
      iCons(
        50,
        iCons(
          43,
          iCons(
            51,
            iCons(42, iCons(52, iCons(45, iCons(53, .IntSeq)))))))
    </k>

  claim [summary-result]:
    <k>
      evalArith(
        runPairCodes(
          .IntSeq,
          vCons(2, vCons(3, vCons(4, vCons(5, .ValSeq)))),
          valSeqConcat(
            vCons(
              str(iCons(43, .IntSeq)),
              vCons(
                str(iCons(42, .IntSeq)),
                vCons(str(iCons(45, .IntSeq)), .ValSeq))),
            vCons(str(.IntSeq), .ValSeq))))
      => 9
    </k>
endmodule
