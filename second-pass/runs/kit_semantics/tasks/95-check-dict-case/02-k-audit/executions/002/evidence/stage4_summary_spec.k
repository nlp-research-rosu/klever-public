requires "verification.k"

module AUDIT-SUMMARY-SPEC
  imports VERIFICATION

  claim [empty]:
    <k> checkCaseSummary(true, true, false, .ValSeq) => false </k>

  claim [lower]:
    <k>
      checkCaseSummary(
        true, true, false,
        vCons(str(iCons(97, .IntSeq)), .ValSeq))
      =>
      true
    </k>

  claim [upper]:
    <k>
      checkCaseSummary(
        true, true, false,
        vCons(str(iCons(65, .IntSeq)), .ValSeq))
      =>
      true
    </k>

  claim [mixed]:
    <k>
      checkCaseSummary(
        true, true, false,
        vCons(
          str(iCons(97, .IntSeq)),
          vCons(str(iCons(66, .IntSeq)), .ValSeq)))
      =>
      false
    </k>

  claim [non-string]:
    <k>
      checkCaseSummary(true, true, false, vCons(8, .ValSeq))
      =>
      false
    </k>
endmodule
