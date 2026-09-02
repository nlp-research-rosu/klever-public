requires "verification-no-bridges.k"

module BRIDGE-CONNECTION-SPEC
  imports VERIFICATION-NO-BRIDGES

  claim [fixed-semantics-doSlice-connection]:
    <k> doSlice(str(CS:IntSeq), noB, noB, someB(-1))
      => str(revIS(CS))
    </k>

  claim [fixed-semantics-buildIS-connection]:
    <k> buildIS(CS:IntSeq, isLen(CS) +Int -1, -1, -1)
      => revIS(CS)
    </k>
endmodule
