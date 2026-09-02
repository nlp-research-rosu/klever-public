requires "/audit-output/evidence/slice-connection-verification.k"

module SLICE-CONNECTION-INDUCTIVE-SPEC
  imports SLICE-CONNECTION

  // Inductive characterization of the fixed buildIS operation for a unit-step
  // slice that starts after the first element.
  claim [drop-tail]:
    <k>
      buildIS(
        iCons(C:Int, R:IntSeq),
        1,
        1 +Int isLen(R),
        1)
      ~> CONT:K
    =>
      R
      ~> CONT
    </k>

  // Full arbitrary-sequence connection needed by the candidate shortcut.
  claim [slice-value]:
    <k>
      buildIS(
        S:IntSeq,
        clampHi(1, isLen(S), 1),
        isLen(S),
        1)
      ~> CONT:K
    =>
      dropOneConnection(S)
      ~> CONT
    </k>
endmodule
