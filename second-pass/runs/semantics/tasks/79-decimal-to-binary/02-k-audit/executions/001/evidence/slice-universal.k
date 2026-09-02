requires "reference-semantics/semantics.k"

module SLICE-UNIVERSAL
  imports MPY

  claim <k> doSlice(
          str(iCons(FIRST, iCons(SECOND, REST))),
          someB(2),
          noB,
          noB)
      => str(REST) </k>
    [label(universal)]
endmodule
