requires "verification.k"

module GROUND-SUMMARY-SPEC
  imports VERIFICATION

  claim
    <k>
      sortThird(.ValSeq)
      =>
      .ValSeq
    </k>

  claim
    <k>
      sortThird(
        vCons(5,
        vCons(6,
        vCons(3,
        vCons(4,
        vCons(8,
        vCons(9,
        vCons(2, .ValSeq))))))))
      =>
      vCons(2,
      vCons(6,
      vCons(3,
      vCons(4,
      vCons(8,
      vCons(9,
      vCons(5, .ValSeq)))))))
    </k>
endmodule
