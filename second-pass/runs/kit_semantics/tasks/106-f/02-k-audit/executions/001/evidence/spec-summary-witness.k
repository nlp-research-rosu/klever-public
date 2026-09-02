requires "verification.k"

module SPEC-SUMMARY-WITNESS
  imports VERIFICATION

  claim
    <k>
      resultRun(.ValSeq, 1, 0, 1, 0)
      => .ValSeq
      ...
    </k>

  claim
    <k>
      resultRun(.ValSeq, 1, 5, 1, 0)
      => vCons(
           1,
           vCons(
             2,
             vCons(
               6,
               vCons(
                 24,
                 vCons(15, .ValSeq)))))
      ...
    </k>
endmodule
