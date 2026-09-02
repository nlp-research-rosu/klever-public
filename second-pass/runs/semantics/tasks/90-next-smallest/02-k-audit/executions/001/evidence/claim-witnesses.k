requires "verification.k"

module AUDIT-CLAIM-WITNESSES
  imports NEXT-SMALLEST-VERIFICATION

  // Concrete substitutions into the universal entry postcondition.
  claim <k> nsScan(nilInts, 0, 0, 0) => noneV </k>
    [label(empty)]

  claim <k> nsScan(consInts(7, nilInts), 0, 0, 0) => noneV </k>
    [label(singleton)]

  claim
    <k> nsScan(consInts(1, consInts(2, nilInts)), 0, 0, 0)
    =>
    2 </k>
    [label(ascending-pair)]

  claim
    <k> nsScan(
      consInts(5,
        consInts(1,
          consInts(4,
            consInts(3,
              consInts(2, nilInts))))),
      0, 0, 0)
    =>
    2 </k>
    [label(documented-permutation)]

  claim
    <k> nsScan(
      consInts(-1,
        consInts(-3,
          consInts(-2,
            consInts(-3, nilInts)))),
      0, 0, 0)
    =>
    -2 </k>
    [label(negative-duplicates)]
endmodule
