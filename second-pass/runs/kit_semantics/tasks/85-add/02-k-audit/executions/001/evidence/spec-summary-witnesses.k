requires "/tmp/audit-work/fresh/verification.k"

module SPEC-SUMMARY-WITNESSES
  imports VERIFICATION

  claim [documented]:
    <k>
      addSummary(
        vCons(4, vCons(2, vCons(6, vCons(7, .ValSeq)))),
        false)
      => 2 ...
    </k>

  claim [negative-even]:
    <k>
      addSummary(
        vCons(1, vCons(-2, vCons(3, vCons(-4, .ValSeq)))),
        false)
      => -6 ...
    </k>

  claim [singleton]:
    <k>
      addSummary(vCons(10, .ValSeq), false)
      => 0 ...
    </k>
endmodule
