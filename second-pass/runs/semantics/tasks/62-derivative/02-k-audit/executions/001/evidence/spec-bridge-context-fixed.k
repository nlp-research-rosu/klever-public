requires "verification-no-bridge.k"

module SPEC-BRIDGE-CONTEXT-FIXED
  imports VERIFICATION-NO-BRIDGE

  claim
    <k>
      truthy(list(enumVS(asValSeq(.IntVals), 0)))
      =>
      false
    </k>
    [label(fixed-empty-enum-truthiness)]
endmodule
