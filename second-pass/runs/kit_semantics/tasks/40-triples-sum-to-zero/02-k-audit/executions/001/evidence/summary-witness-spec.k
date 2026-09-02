requires "verification.k"

module SUMMARY-WITNESS-SPEC
  imports VERIFICATION

  claim [summary-true-000]:
    <k>
      tripleFrom(iCons(0, iCons(0, iCons(0, .IntSeq))), 0)
      => true
    </k>

  claim [summary-false-12]:
    <k>
      tripleFrom(iCons(1, iCons(2, .IntSeq)), 0)
      => false
    </k>
endmodule
