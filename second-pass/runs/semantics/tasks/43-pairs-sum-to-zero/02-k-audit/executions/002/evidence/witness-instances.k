requires "/tmp/audit-work/verification.k"

module REVIEWER-WITNESS-INSTANCES
  imports PAIRS-VERIFICATION

  claim [empty-result]:
    <k> pairsIS(.IntSeq) => false </k>

  claim [single-zero-result]:
    <k> pairsIS(iCons(0, .IntSeq)) => false </k>

  claim [distinct-opposites-result]:
    <k> pairsIS(iCons(5, iCons(-5, .IntSeq))) => true </k>

  claim [late-opposites-result]:
    <k>
      pairsIS(iCons(2, iCons(4, iCons(-5, iCons(3, iCons(5, iCons(7, .IntSeq)))))))
      =>
      true
    </k>

  claim [no-opposites-result]:
    <k> pairsIS(iCons(1, iCons(2, iCons(3, .IntSeq)))) => false </k>
endmodule
