requires "verification.k"

module SPEC-BRIDGE-GROUND-CANDIDATE-FALSE
  imports VERIFICATION

  // Ground instance VS = .IntVals under the same candidate theory.
  claim
    <k>
      truthy(list(enumVS(asValSeq(.IntVals), 0)))
      =>
      false
    </k>
    [label(candidate-ground-empty-is-empty)]
endmodule
