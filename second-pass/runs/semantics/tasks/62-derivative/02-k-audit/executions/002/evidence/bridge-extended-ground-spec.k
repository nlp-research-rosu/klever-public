requires "verification.k"

module BRIDGE-EXTENDED-GROUND-SPEC
  imports VERIFICATION

  claim
    <k>
      truthy(list(enumVS(asValSeq(.IntVals), 0)))
      => true
    </k>
    [label(extended-empty-enumerate-is-true)]
endmodule
