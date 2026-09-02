requires "bridge-fixed.k"

module BRIDGE-FIXED-SPEC
  imports BRIDGE-FIXED

  claim
    <k>
      truthy(list(enumVS(asValSeq(.IntVals), 0)))
      => false
    </k>
    [label(fixed-empty-enumerate-is-false)]
endmodule
