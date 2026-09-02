requires "verification.k"

module AUDIT-BRIDGE-CONTINUATION
  imports VERIFICATION

  claim [bridge-preserves-suffix]:
    <k>
      seqLen(str(iCons(97, .IntSeq))) ~> 41
      => 1 ~> 41
    </k>
endmodule
