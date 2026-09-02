requires "reference-semantics/semantics.k"

module SLICE-GROUND
  imports MPY

  claim <k> doSlice(
          str(iCons(65, iCons(66, .IntSeq))),
          someB(2),
          noB,
          noB)
      => str(.IntSeq) </k>
    [label(empty-tail)]

  claim <k> doSlice(
          str(iCons(65, iCons(66, iCons(67, .IntSeq)))),
          someB(2),
          noB,
          noB)
      => str(iCons(67, .IntSeq)) </k>
    [label(one-tail)]

  claim <k> doSlice(
          str(iCons(1, iCons(2, iCons(3, iCons(4, iCons(5, .IntSeq)))))),
          someB(2),
          noB,
          noB)
      => str(iCons(3, iCons(4, iCons(5, .IntSeq)))) </k>
    [label(three-tail)]
endmodule
