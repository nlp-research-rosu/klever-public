requires "verification.k"

module SPEC-SEMANTIC-WITNESS
  imports VERIFICATION

  claim [bool-int-summary]:
    <k>
      commonSpec(
        vCons(true, .ValSeq),
        vCons(1, .ValSeq)
      )
    =>
      .ValSeq
    </k>

  claim [int-float-summary]:
    <k>
      commonSpec(
        vCons(1, .ValSeq),
        vCons(1.0, .ValSeq)
      )
    =>
      .ValSeq
    </k>
endmodule
