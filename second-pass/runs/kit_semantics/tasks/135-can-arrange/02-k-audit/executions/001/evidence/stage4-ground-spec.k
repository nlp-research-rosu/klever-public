requires "verification.k"

module REVIEWER-GROUND-SPEC
  imports VERIFICATION

  claim [empty-summary]:
    <k> arrangeSeq(.ValSeq, 0, 0, -1) => -1 </k>

  claim [documented-summary]:
    <k>
      arrangeSeq(
        vCons(1, vCons(2, vCons(4, vCons(3, vCons(5, .ValSeq))))),
        0,
        0,
        -1)
      => 3
    </k>
endmodule
