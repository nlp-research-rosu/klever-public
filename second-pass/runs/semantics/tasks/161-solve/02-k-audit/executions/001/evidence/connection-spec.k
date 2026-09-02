requires "reference-semantics/semantics.k"

module CONNECTION-SPEC
  imports MPY

  // Bridge-free universal obligations for both candidate simplifications.
  claim [reverse-builder-connection]:
    <k> buildIS(CS:IntSeq, isLen(CS) +Int -1, -1, -1)
      => revIS(CS)
    </k>

  claim [reverse-slice-connection]:
    <k> doSlice(str(CS:IntSeq), noB, noB, someB(-1))
      => str(revIS(CS))
    </k>
endmodule
