requires "/tmp/audit-work/142-sum-squares-audit/verification.k"

module GROUND-SUMMARY
  imports SUM-SQUARES-VERIFICATION

  claim [empty]:
    <k>
      sumSquares(.Ints, 0, 0)
      => 0
    </k>

  claim [example-positive]:
    <k>
      sumSquares(
        intCons(1, intCons(2, intCons(3, .Ints))),
        0,
        0)
      => 6
    </k>

  claim [example-negative]:
    <k>
      sumSquares(
        intCons(-1, intCons(-5, intCons(2, intCons(-1, intCons(-5, .Ints))))),
        0,
        0)
      => -126
    </k>

  claim [branch-boundaries]:
    <k>
      sumSquares(
        intCons(1,
        intCons(2,
        intCons(3,
        intCons(4,
        intCons(5,
        intCons(6,
        intCons(7,
        intCons(8,
        intCons(9,
        intCons(10,
        intCons(11,
        intCons(12,
        intCons(13, .Ints))))))))))))),
        0,
        0)
      => 1231
    </k>
endmodule
