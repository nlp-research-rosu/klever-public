requires "/audit-output/evidence/slice-connection-verification.k"

module SLICE-CONNECTION-SPEC
  imports SLICE-CONNECTION

  // Bridge-free fixed-semantics execution under an arbitrary continuation.
  claim <k>
    Subscript(
      str(S:IntSeq),
      Slice(Int(1), NoBound, NoBound))
    ~> CONT:K
  =>
    str(dropOneConnection(S))
    ~> CONT
  </k>
endmodule
