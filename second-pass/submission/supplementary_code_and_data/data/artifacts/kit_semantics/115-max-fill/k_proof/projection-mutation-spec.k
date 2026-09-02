requires "verification.k"

module MAX-FILL-PROJECTION-MUTATION-SPEC
  imports MAX-FILL-SUMMARY

  // Both claims deliberately demand the opposite of a defining collapse rule.
  claim [wrong-int]:
    <k> .K </k>
    ensures projectInt(1) ==Int 0

  claim [wrong-row]:
    <k> .K </k>
    ensures rowVals(list(vCons(1, .ValSeq))) ==K .ValSeq
endmodule
