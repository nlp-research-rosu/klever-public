requires "verification.k"

module WITNESS-SPEC
  imports NEXT-SMALLEST-WITH-LOOP-LEMMA

  claim
    <k>
      nsScan(
        consInts(3, consInts(1, consInts(2, consInts(1, nilInts)))),
        0,
        0,
        0)
    =>
      2
    </k>
endmodule
