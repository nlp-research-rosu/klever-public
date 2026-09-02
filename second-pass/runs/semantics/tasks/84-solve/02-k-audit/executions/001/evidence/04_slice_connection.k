requires "/tmp/audit-work/candidate-src/reference-semantics/semantics.k"

module SLICE-CONNECTION
  imports MPY

  // Bridge-free universal connection theorem for verification.k:31-38.
  // CONT is arbitrary, so the theorem checks the complete continuation domain
  // accepted by the local operational bridge.
  claim
    <k>
      Subscript(
        str(iCons(48, iCons(98, REST:IntSeq))),
        Slice(Int(2), NoBound, NoBound)
      ) ~> CONT:K
      =>
      str(REST) ~> CONT
    </k>
endmodule
