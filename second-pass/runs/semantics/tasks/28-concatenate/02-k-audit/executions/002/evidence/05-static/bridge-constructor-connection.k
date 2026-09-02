requires "verification-no-bridge.k"

module BRIDGE-CONSTRUCTOR-CONNECTION
  imports CONCATENATE-NO-BRIDGE

  // Constructor form of the same domain. The two exhaustive isStringValueNB
  // equations make its ground instances exactly the guard-domain instances.
  claim [constructor-domain]:
    <k>
      applyBin("+", str(A:IntSeq), str(B:IntSeq))
      =>
      str(seqConcat(A, stringCodesNB(str(B))))
    </k>
endmodule
