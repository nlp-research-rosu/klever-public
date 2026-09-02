requires "connection.k"

module AUDIT-SUMMARY-WITNESS
  imports CONNECTION

  claim [empty]:
    <k>
      checkCaseSummary(true, true, false, .ValSeq)
      =>
      false
    </k>

  claim [all-lower]:
    <k>
      checkCaseSummary(
        true,
        true,
        false,
        vCons(
          str(iCons(97, .IntSeq)),
          vCons(str(iCons(98, iCons(50, .IntSeq))), .ValSeq)))
      =>
      true
    </k>

  // This key sequence satisfies SPEC.target's no-reference premise.  It is
  // also the smallest explicit candidate/canonical divergence found by the
  // independent differential: A, B, then c.
  claim [late-mixed]:
    <k>
      checkCaseSummary(
        true,
        true,
        false,
        vCons(
          str(iCons(65, .IntSeq)),
          vCons(
            str(iCons(66, .IntSeq)),
            vCons(str(iCons(99, .IntSeq)), .ValSeq))))
      =>
      false
    </k>

  claim [unicode-lower-model-result]:
    <k>
      checkCaseSummary(
        true,
        true,
        false,
        vCons(str(iCons(233, .IntSeq)), .ValSeq))
      =>
      false
    </k>
endmodule
