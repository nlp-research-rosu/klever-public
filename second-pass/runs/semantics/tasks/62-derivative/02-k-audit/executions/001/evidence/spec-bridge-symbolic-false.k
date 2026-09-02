requires "verification.k"

module SPEC-BRIDGE-SYMBOLIC-FALSE
  imports VERIFICATION

  // This universal conclusion is false at VS = .IntVals under the supplied
  // semantics. If it closes, the over-broad simplification is unsound.
  claim
    <k>
      truthy(list(enumVS(asValSeq(VS:IntVals), 0)))
      =>
      true
    </k>
    [label(symbolic-enum-always-nonempty)]
endmodule
