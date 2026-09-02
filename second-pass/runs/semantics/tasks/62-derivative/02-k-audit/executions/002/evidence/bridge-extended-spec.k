requires "verification.k"

module BRIDGE-EXTENDED-SPEC
  imports VERIFICATION

  claim
    <k>
      truthy(list(enumVS(asValSeq(VS:IntVals), 0)))
      => true
    </k>
    [label(extended-enumerate-always-true)]
endmodule
