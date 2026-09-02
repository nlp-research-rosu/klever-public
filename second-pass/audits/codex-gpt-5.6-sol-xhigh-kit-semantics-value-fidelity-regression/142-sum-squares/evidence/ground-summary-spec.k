requires "verification.k"

module GROUND-SUMMARY-SPEC
  imports VERIFICATION

  claim [precondition-witness]:
    <k>
      allInts(vCons(1, vCons(2, vCons(3, .ValSeq))))
      => true
    </k>

  claim [prompt-example-1]:
    <k>
      sumSquares(vCons(1, vCons(2, vCons(3, .ValSeq))), 0, 0)
      => 6
    </k>

  claim [prompt-example-empty]:
    <k> sumSquares(.ValSeq, 0, 0) => 0 </k>

  claim [prompt-example-negative]:
    <k>
      sumSquares(
        vCons(-1, vCons(-5, vCons(2, vCons(-1, vCons(-5, .ValSeq))))),
        0,
        0)
      => -126
    </k>

  claim [index-12-overlap]:
    <k>
      sumSquares(
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(1,
        vCons(-3, .ValSeq))))))))))))),
        0,
        0)
      => 21
    </k>
endmodule
