requires "verification.k"

module SPEC-HELPER-VALUES
  imports VERIFICATION

  claim [projection-positive]:
    <k> projectIntTotal(2) => 2 ... </k>

  claim [projection-negative]:
    <k> projectIntTotal(-3) => -3 ... </k>

  claim [sum-ground]:
    <k> sumFrom(vCons(2, vCons(-3, .ValSeq)), 0) => -1 ... </k>

  claim [product-ground]:
    <k> productFrom(vCons(2, vCons(-3, .ValSeq)), 1) => -6 ... </k>
endmodule
