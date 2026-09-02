requires "verification.k"

module SLICE-WRONG
  imports VERIFICATION

  claim <k> doSlice(
          str(iCons(65, iCons(66, iCons(67, .IntSeq)))),
          someB(2),
          noB,
          noB)
      => str(.IntSeq) </k>
    [label(wrong-one-tail)]
endmodule
