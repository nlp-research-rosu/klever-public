requires "verification.k"

module SPEC-BRIDGE-CONTEXT-CANDIDATE
  imports VERIFICATION

  claim
    <k>
      truthy(list(enumVS(asValSeq(.IntVals), 0)))
      =>
      true
    </k>
    [label(candidate-empty-enum-truthiness)]
endmodule
