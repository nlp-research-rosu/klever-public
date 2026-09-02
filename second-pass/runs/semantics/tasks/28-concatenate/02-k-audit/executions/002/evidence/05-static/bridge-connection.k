requires "verification-no-bridge.k"

module BRIDGE-CONNECTION
  imports CONCATENATE-NO-BRIDGE

  // Universal connection theorem over the complete guard of the candidate's
  // added applyBin rule, using only fixed semantics plus independently defined
  // constructor predicates/projection. The candidate bridge is not imported.
  claim [guard-domain]:
    <k>
      applyBin("+", str(A:IntSeq), V:Val)
      =>
      str(seqConcat(A, stringCodesNB(V)))
    </k>
    requires isStringValueNB(V)
endmodule
