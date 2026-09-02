requires "/tmp/audit-work/rebuild/verification.k"

module GROUND-RESULT-SPEC
  imports VERIFICATION-BASE

  claim [empty]:
    <k>
      expectedResult(.IntSeq, .ValSeq)
      => str(iCons(46, .IntSeq))
    </k>

  claim [ascii]:
    <k>
      expectedResult(
        iCons(67, .IntSeq),
        vCons(
          str(iCons(65, .IntSeq)),
          vCons(str(iCons(98, .IntSeq)), .ValSeq)
        )
      )
      => str(iCons(67, iCons(46, iCons(65, .IntSeq))))
    </k>

  // In the supplied ASCII model, Greek capital omega contributes score 0.
  claim [greek-model-boundary]:
    <k>
      expectedResult(
        iCons(67, .IntSeq),
        vCons(
          str(iCons(65, .IntSeq)),
          vCons(
            str(iCons(937, iCons(937, .IntSeq))),
            .ValSeq
          )
        )
      )
      => str(iCons(67, iCons(46, iCons(65, .IntSeq))))
    </k>

  // Roman numeral one is likewise not an ASCII uppercase letter.
  claim [roman-candidate-defect]:
    <k>
      expectedResult(
        iCons(67, .IntSeq),
        vCons(
          str(iCons(65, .IntSeq)),
          vCons(
            str(iCons(8544, iCons(8544, .IntSeq))),
            .ValSeq
          )
        )
      )
      => str(iCons(67, iCons(46, iCons(65, .IntSeq))))
    </k>
endmodule
