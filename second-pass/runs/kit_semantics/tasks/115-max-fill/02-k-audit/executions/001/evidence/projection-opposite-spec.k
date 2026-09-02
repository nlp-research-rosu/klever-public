requires "verification.k"

module REVIEWER-PROJECTION-OPPOSITE-SPEC
  imports MAX-FILL-SUMMARY

  // Deliberately false opposite ground interpretations of the two opaque
  // projection symbols.  Their guarded/collapse equations must reject both.
  claim [opposite-int]:
    <k> .K </k>
    ensures projectInt(1) ==Int 0

  claim [opposite-row]:
    <k> .K </k>
    ensures
      rowVals(list(vCons(1, .ValSeq))) ==K .ValSeq
endmodule
